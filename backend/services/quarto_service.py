"""Regras de negócio relacionadas aos quartos do hotel."""

from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta
from typing import Dict, Iterable, List, Optional

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.quarto import Quarto
from models.reserva import Reserva
from schemas.quarto import (
    QuartoCalendar,
    QuartoCalendarDay,
    QuartoCreate,
    QuartoUpdate,
)
from services.reserva_service import STATUS_CANCELADA, STATUS_EQUIVALENTS

_CANCELLED_STATUSES: Iterable[str] = STATUS_EQUIVALENTS[STATUS_CANCELADA]


def _ensure_date_range(data_inicio: date, data_fim: date) -> None:
    """Garante que o intervalo de datas é válido."""
    if data_inicio > data_fim:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="data_inicio deve ser anterior ou igual a data_fim",
        )


def _build_day_entries(
    reservas: List[Reserva],
    data_inicio: date,
    data_fim: date,
) -> List[QuartoCalendarDay]:
    """Gera a ocupação diária de um quarto para o período solicitado."""
    total_dias = (data_fim - data_inicio).days + 1
    ocupacao_por_dia: Dict[date, Reserva] = {}

    for reserva in reservas:
        inicio = max(reserva.data_checkin, data_inicio)
        fim = min(reserva.data_checkout, data_fim + timedelta(days=1))
        dia_atual = inicio
        while dia_atual < fim:
            ocupacao_por_dia[dia_atual] = reserva
            dia_atual += timedelta(days=1)

    dias: List[QuartoCalendarDay] = []
    for offset in range(total_dias):
        dia = data_inicio + timedelta(days=offset)
        reserva = ocupacao_por_dia.get(dia)
        if reserva:
            # Determinar o status do dia baseado na reserva
            if dia == reserva.data_checkin:
                day_status = "checkin"
            elif dia == reserva.data_checkout:
                day_status = "checkout"
            else:
                day_status = "ocupado"
            
            dias.append(
                QuartoCalendarDay(
                    data=dia,
                    status=day_status,
                    reserva_id=reserva.id,
                    reserva_status=reserva.status,
                    cliente_id=reserva.client_id,
                )
            )
        else:
            dias.append(QuartoCalendarDay(data=dia, status="livre"))

    return dias


def create_quarto(db: Session, quarto_data: QuartoCreate) -> Quarto:
    """Cria um novo quarto garantindo número único."""
    existente = (
        db.query(Quarto).filter(Quarto.numero == quarto_data.numero).first()
    )
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um quarto cadastrado com esse número.",
        )

    db_quarto = Quarto(**quarto_data.model_dump())
    db.add(db_quarto)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não foi possível criar o quarto. Verifique se o número é único.",
        ) from exc

    db.refresh(db_quarto)
    return db_quarto


def get_quarto(db: Session, quarto_id: int) -> Optional[Quarto]:
    """Busca um quarto pelo ID."""
    return db.query(Quarto).filter(Quarto.id == quarto_id).first()


def get_quartos(db: Session, skip: int = 0, limit: int = 100) -> List[Quarto]:
    """Lista quartos cadastrados com paginação."""
    return (
        db.query(Quarto)
        .order_by(Quarto.numero)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_quarto(
    db: Session,
    quarto_id: int,
    quarto_update: QuartoUpdate,
) -> Optional[Quarto]:
    """Atualiza dados de um quarto existente."""
    db_quarto = get_quarto(db, quarto_id)
    if not db_quarto:
        return None

    update_data = quarto_update.model_dump(exclude_unset=True)

    if "numero" in update_data:
        outro = (
            db.query(Quarto)
            .filter(Quarto.numero == update_data["numero"], Quarto.id != quarto_id)
            .first()
        )
        if outro:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe outro quarto com esse número.",
            )

    if "valor_diaria" in update_data and update_data["valor_diaria"] is not None:
        try:
            update_data["valor_diaria"] = float(update_data["valor_diaria"])
        except (TypeError, ValueError) as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="valor_diaria inválido. Utilize números.",
            ) from exc

    for campo, valor in update_data.items():
        setattr(db_quarto, campo, valor)

    db.commit()
    db.refresh(db_quarto)
    return db_quarto


def delete_quarto(db: Session, quarto_id: int) -> bool:
    """Remove um quarto se não houver reservas ativas associadas."""
    db_quarto = get_quarto(db, quarto_id)
    if not db_quarto:
        return False

    reservas_ativas = (
        db.query(Reserva)
        .filter(
            Reserva.quarto_id == quarto_id,
            Reserva.status.notin_(tuple(_CANCELLED_STATUSES)),
        )
        .count()
    )

    if reservas_ativas:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível remover o quarto com reservas ativas.",
        )

    db.delete(db_quarto)
    db.commit()
    return True


def get_calendario_ocupacao(
    db: Session,
    data_inicio: date,
    data_fim: date,
) -> List[QuartoCalendar]:
    """Retorna a ocupação de todos os quartos no período informado."""
    _ensure_date_range(data_inicio, data_fim)

    quartos = db.query(Quarto).order_by(Quarto.numero).all()
    if not quartos:
        return []

    reservas = (
        db.query(Reserva)
        .filter(
            Reserva.status.notin_(tuple(_CANCELLED_STATUSES)),
            Reserva.data_checkin < data_fim + timedelta(days=1),
            Reserva.data_checkout > data_inicio,
        )
        .all()
    )

    reservas_por_quarto: Dict[int, List[Reserva]] = defaultdict(list)
    for reserva in reservas:
        reservas_por_quarto[reserva.quarto_id].append(reserva)

    calendario: List[QuartoCalendar] = []
    for quarto in quartos:
        dias = _build_day_entries(
            reservas_por_quarto.get(quarto.id, []),
            data_inicio,
            data_fim,
        )
        
        # Se o quarto está marcado como "ocupado", marcar todos os dias como ocupados
        if quarto.status == "ocupado":
            for dia in dias:
                if dia.status == "livre":
                    dia.status = "ocupado"
        
        calendario.append(
            QuartoCalendar(
                quarto_id=quarto.id,
                numero=quarto.numero,
                tipo=quarto.tipo,
                status=quarto.status,
                capacidade=quarto.capacidade,
                valor_diaria=float(quarto.valor_diaria),
                periodo_inicio=data_inicio,
                periodo_fim=data_fim,
                ocupacao=dias,
            )
        )

    return calendario
