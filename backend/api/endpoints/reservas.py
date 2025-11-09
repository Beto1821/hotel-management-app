from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core.database import get_db
from dependencies.auth import get_current_active_user
from models.user_model import User
from schemas.reserva import Reserva, ReservaCreate, ReservaUpdate
from services import reserva_service


router = APIRouter()


@router.post("/", response_model=Reserva, status_code=status.HTTP_201_CREATED)
def create_reserva(
    reserva: ReservaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Cria uma nova reserva."""
    return reserva_service.create_reserva(db=db, reserva=reserva)


@router.get("/", response_model=List[Reserva])
def read_reservas(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(default=None, description="Filtra reservas por status"),
    mes: Optional[str] = Query(
        default=None,
        description="Filtra reservas pelo mês de check-in no formato YYYY-MM",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Lista reservas com filtros opcionais de status e mês."""
    reservas = reserva_service.get_reservas(
        db,
        skip=skip,
        limit=limit,
        status_filter=status,
        mes=mes,
    )
    return reservas


@router.get("/{reserva_id}", response_model=Reserva)
def read_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Busca uma reserva específica."""
    db_reserva = reserva_service.get_reserva(db, reserva_id=reserva_id)
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return db_reserva


@router.put("/{reserva_id}", response_model=Reserva)
def update_reserva(
    reserva_id: int,
    reserva: ReservaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Atualiza uma reserva."""
    db_reserva = reserva_service.update_reserva(
        db, reserva_id=reserva_id, reserva_update=reserva
    )
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return db_reserva


@router.delete("/{reserva_id}", response_model=Reserva)
def delete_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Cancela uma reserva (altera o status para 'cancelada')."""
    db_reserva = reserva_service.delete_reserva(db, reserva_id=reserva_id)
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return db_reserva
