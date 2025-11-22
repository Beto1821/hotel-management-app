"""Regras de negócio relacionadas às reservas."""

from datetime import date
from typing import List, Optional, Tuple

from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session, selectinload

from models.reserva import Reserva
from models.quarto import Quarto
from schemas.reserva import ReservaCreate, ReservaUpdate

STATUS_PENDENTE = "pendente"
STATUS_ATIVA = "ativa"
STATUS_CONCLUIDA = "concluida"
STATUS_CANCELADA = "cancelada"

STATUS_EQUIVALENTS = {
    STATUS_PENDENTE: {STATUS_PENDENTE, "confirmado", "confirmada"},
    STATUS_ATIVA: {STATUS_ATIVA, "ativo", "em_andamento"},
    STATUS_CONCLUIDA: {
        STATUS_CONCLUIDA,
        "concluido",
        "concluida",
        "finalizado",
    },
    STATUS_CANCELADA: {STATUS_CANCELADA, "cancelado", "cancelada"},
}


def is_quarto_disponivel(
    db: Session,
    quarto_id: int,
    data_checkin: date,
    data_checkout: date,
    reserva_id_a_ignorar: Optional[int] = None,
) -> bool:
    """Verifica se um quarto está disponível no período informado."""
    query = db.query(Reserva).filter(
        Reserva.quarto_id == quarto_id,
        Reserva.status.notin_(tuple(STATUS_EQUIVALENTS[STATUS_CANCELADA])),
        and_(
            Reserva.data_checkin < data_checkout,
            Reserva.data_checkout > data_checkin,
        ),
    )

    if reserva_id_a_ignorar:
        query = query.filter(Reserva.id != reserva_id_a_ignorar)

    return query.first() is None


def calcular_valor_total(
    db: Session,
    quarto_id: int,
    data_checkin: date,
    data_checkout: date,
) -> float:
    """Calcula o valor total da estadia com base na diária e número de noites."""
    if data_checkin >= data_checkout:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A data de check-out deve ser posterior à data de check-in.",
        )

    quarto = db.query(Quarto).filter(Quarto.id == quarto_id).first()
    if not quarto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quarto não encontrado.",
        )

    numero_de_noites = (data_checkout - data_checkin).days
    return quarto.valor_diaria * numero_de_noites


def create_reserva(db: Session, reserva: ReservaCreate) -> Reserva:
    """Cria uma reserva após validar disponibilidade e calcular o valor."""
    if not is_quarto_disponivel(
        db, reserva.quarto_id, reserva.data_checkin, reserva.data_checkout
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="O quarto não está disponível para as datas selecionadas.",
        )

    valor_total = calcular_valor_total(
        db, reserva.quarto_id, reserva.data_checkin, reserva.data_checkout
    )

    db_reserva = Reserva(
        quarto_id=reserva.quarto_id,
        client_id=reserva.client_id,
        data_checkin=reserva.data_checkin,
        data_checkout=reserva.data_checkout,
        valor_total=valor_total,
        status=STATUS_PENDENTE,
    )
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva


def get_reserva(db: Session, reserva_id: int) -> Optional[Reserva]:
    """Busca uma reserva pelo ID."""
    return (
        db.query(Reserva)
        .options(
            selectinload(Reserva.quarto),
            selectinload(Reserva.client),
        )
        .filter(Reserva.id == reserva_id)
        .first()
    )


def _parse_month_filter(mes: str) -> Tuple[date, date]:
    try:
        year_str, month_str = mes.split("-")
        year = int(year_str)
        month = int(month_str)
        start = date(year, month, 1)
    except (ValueError, AttributeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parâmetro 'mes' inválido. Use o formato YYYY-MM.",
        ) from exc

    end = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    return start, end


def get_reservas(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    mes: Optional[str] = None,
) -> List[Reserva]:
    """Lista reservas com filtros opcionais de status e mês."""
    query = (
        db.query(Reserva)
        .options(
            selectinload(Reserva.quarto),
            selectinload(Reserva.client),
        )
        .order_by(Reserva.data_checkin.desc())
    )

    if status_filter:
        acceptable_statuses = STATUS_EQUIVALENTS.get(status_filter, {status_filter})
        query = query.filter(Reserva.status.in_(tuple(acceptable_statuses)))

    if mes:
        start, end = _parse_month_filter(mes)
        query = query.filter(
            Reserva.data_checkin >= start,
            Reserva.data_checkin < end,
        )

    return query.offset(skip).limit(limit).all()


def update_reserva(
    db: Session,
    reserva_id: int,
    reserva_update: ReservaUpdate,
) -> Optional[Reserva]:
    """Atualiza campos mutáveis de uma reserva existente."""
    db_reserva = get_reserva(db, reserva_id)
    if not db_reserva:
        return None

    update_data = reserva_update.model_dump(exclude_unset=True, by_alias=True)

    new_checkin = update_data.get("data_checkin", db_reserva.data_checkin)
    new_checkout = update_data.get("data_checkout", db_reserva.data_checkout)

    if "data_checkin" in update_data or "data_checkout" in update_data:
        if not is_quarto_disponivel(
            db,
            db_reserva.quarto_id,
            new_checkin,
            new_checkout,
            reserva_id_a_ignorar=reserva_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="O quarto não está disponível para as novas datas.",
            )
        update_data["valor_total"] = calcular_valor_total(
            db, db_reserva.quarto_id, new_checkin, new_checkout
        )

    if "status" in update_data:
        db_reserva.status = update_data["status"]

    if "data_checkin" in update_data:
        db_reserva.data_checkin = new_checkin

    if "data_checkout" in update_data:
        db_reserva.data_checkout = new_checkout

    if "valor_total" in update_data:
        db_reserva.valor_total = update_data["valor_total"]

    db.commit()
    db.refresh(db_reserva)
    return db_reserva


def check_in_reserva(db: Session, reserva_id: int) -> Reserva:
    reserva = get_reserva(db, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada.")

    if reserva.status not in STATUS_EQUIVALENTS[STATUS_PENDENTE]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A reserva não pode realizar check-in no status atual.",
        )

    reserva.status = STATUS_ATIVA
    db.commit()
    db.refresh(reserva)
    return reserva


def check_out_reserva(db: Session, reserva_id: int) -> Reserva:
    reserva = get_reserva(db, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada.")

    if reserva.status not in STATUS_EQUIVALENTS[STATUS_ATIVA]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A reserva não pode ser concluída a partir do status atual.",
        )

    reserva.status = STATUS_CONCLUIDA
    db.commit()
    db.refresh(reserva)
    return reserva


def cancel_reserva(db: Session, reserva_id: int) -> Reserva:
    reserva = get_reserva(db, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada.")

    if reserva.status in STATUS_EQUIVALENTS[STATUS_CONCLUIDA]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Reservas concluídas não podem ser canceladas.",
        )

    reserva.status = STATUS_CANCELADA
    db.commit()
    db.refresh(reserva)
    return reserva


def delete_reserva(db: Session, reserva_id: int) -> Optional[Reserva]:
    """Mantém compatibilidade cancelando a reserva em vez de excluí-la."""
    try:
        return cancel_reserva(db, reserva_id)
    except HTTPException as exc:
        if exc.status_code == 404:
            return None
        raise
