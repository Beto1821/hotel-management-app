from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.audit_log import AuditLog
from models.user_model import User
from models.client_model import Client
from models.reserva import Reserva
from models.quarto import Quarto
from dependencies.auth import get_current_user

router = APIRouter()

@router.get("/")
async def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retorna estatísticas do dashboard."""
    
    # Contar registros
    total_clients = db.query(Client).count()
    total_quartos = db.query(Quarto).count()
    total_reservas = db.query(Reserva).count()
    
    # Quartos ocupados (reservas ativas)
    occupied_rooms = db.query(Reserva).filter(Reserva.status == 'CONFIRMADA').count()
    
    return {
        "stats": {
            "total_clients": total_clients,
            "active_reservas": total_reservas,
            "occupied_rooms": occupied_rooms,
            "total_rooms": total_quartos,
            "monthly_revenue": 0.0
        },
        "recent_activities": []
    }

@router.get("/activities")
async def get_recent_activities(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retorna as últimas atividades do sistema."""
    
    # Buscar últimas atividades
    activities = db.query(AuditLog)\
        .order_by(AuditLog.timestamp.desc())\
        .limit(limit)\
        .all()
    
    # Formatar resposta
    return [
        {
            "id": activity.id,
            "action": activity.action,
            "user_id": activity.user_id,
            "resource": activity.resource,
            "timestamp": activity.timestamp.isoformat(),
            "ip_address": activity.ip_address,
            "details": activity.details
        }
        for activity in activities
    ]
