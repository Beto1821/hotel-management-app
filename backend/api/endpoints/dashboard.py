from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.audit_log import AuditLog
from models.user_model import User
from dependencies.auth import get_current_user

router = APIRouter()

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
