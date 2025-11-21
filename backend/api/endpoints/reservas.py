from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from sqlalchemy.orm import Session

from core.database import get_db
from dependencies.auth import get_current_active_user
from models.user_model import User
from schemas.reserva import Reserva, ReservaCreate, ReservaUpdate
from services import reserva_service
from services.audit_service import AuditService
from utils.request_utils import get_client_info


router = APIRouter()


@router.post("/", response_model=Reserva, status_code=status.HTTP_201_CREATED)
def create_reserva(
    reserva: ReservaCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Cria uma nova reserva."""
    new_reserva = reserva_service.create_reserva(db=db, reserva=reserva)
    
    # Registrar auditoria
    try:
        client_info = get_client_info(request)
        AuditService.log_action(
            db=db,
            user_id=current_user.id,
            action="CREATE_RESERVATION",
            resource="RESERVATION",
            resource_id=new_reserva.id,
            ip_address=client_info["ip_address"],
            user_agent=client_info["user_agent"],
            details={"client_id": new_reserva.cliente_id, "quarto_id": new_reserva.quarto_id}
        )
    except Exception as e:
        print(f"Erro ao registrar auditoria: {e}")
    
    return new_reserva


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
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Atualiza uma reserva."""
    db_reserva = reserva_service.update_reserva(
        db, reserva_id=reserva_id, reserva_update=reserva
    )
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    
    # Registrar auditoria
    try:
        client_info = get_client_info(request)
        AuditService.log_action(
            db=db,
            user_id=current_user.id,
            action="UPDATE_RESERVATION",
            resource="RESERVATION",
            resource_id=db_reserva.id,
            ip_address=client_info["ip_address"],
            user_agent=client_info["user_agent"],
            details={"status": db_reserva.status}
        )
    except Exception as e:
        print(f"Erro ao registrar auditoria: {e}")

    
    return db_reserva


@router.delete("/{reserva_id}", response_model=Reserva)
def delete_reserva(
    reserva_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Cancela uma reserva (altera o status para 'cancelada')."""
    db_reserva = reserva_service.delete_reserva(db, reserva_id=reserva_id)
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    
    # Registrar auditoria
    try:
        client_info = get_client_info(request)
        AuditService.log_action(
            db=db,
            user_id=current_user.id,
            action="DELETE_RESERVATION",
            resource="RESERVATION",
            resource_id=db_reserva.id,
            ip_address=client_info["ip_address"],
            user_agent=client_info["user_agent"],
            details={"status": "CANCELADA"}
        )
    except Exception as e:
        print(f"Erro ao registrar auditoria: {e}")

    
    return db_reserva
