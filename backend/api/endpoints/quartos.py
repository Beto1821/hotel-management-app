"""Endpoints da API para gerenciamento de quartos."""

from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core.database import get_db
from dependencies.auth import get_current_active_user
from models.user_model import User
from schemas.quarto import (
    Quarto,
    QuartoCalendar,
    QuartoCreate,
    QuartoUpdate,
)
from services import quarto_service

router = APIRouter()


@router.post("/", response_model=Quarto, status_code=status.HTTP_201_CREATED)
def create_quarto(
    quarto: QuartoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Quarto:
    """Cria um novo quarto."""
    return quarto_service.create_quarto(db=db, quarto_data=quarto)


@router.get("/", response_model=List[Quarto])
def list_quartos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[Quarto]:
    """Lista quartos cadastrados."""
    return quarto_service.get_quartos(db=db, skip=skip, limit=limit)


@router.get("/calendario", response_model=List[QuartoCalendar])
def get_calendario(
    data_inicio: date = Query(
        ..., description="Data inicial no formato YYYY-MM-DD"
    ),
    data_fim: date = Query(
        ..., description="Data final no formato YYYY-MM-DD"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[QuartoCalendar]:
    """Retorna a ocupação dos quartos em um intervalo de datas."""
    return quarto_service.get_calendario_ocupacao(
        db=db,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


@router.get("/{quarto_id}", response_model=Quarto)
def get_quarto(
    quarto_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Quarto:
    """Retorna um quarto específico."""
    db_quarto = quarto_service.get_quarto(db=db, quarto_id=quarto_id)
    if not db_quarto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quarto não encontrado",
        )
    return db_quarto


@router.put("/{quarto_id}", response_model=Quarto)
def update_quarto(
    quarto_id: int,
    quarto_update: QuartoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Quarto:
    """Atualiza os dados de um quarto."""
    db_quarto = quarto_service.update_quarto(
        db=db,
        quarto_id=quarto_id,
        quarto_update=quarto_update,
    )
    if not db_quarto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quarto não encontrado",
        )
    return db_quarto


@router.delete("/{quarto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quarto(
    quarto_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """Remove um quarto sem reservas ativas."""
    deleted = quarto_service.delete_quarto(db=db, quarto_id=quarto_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quarto não encontrado",
        )
