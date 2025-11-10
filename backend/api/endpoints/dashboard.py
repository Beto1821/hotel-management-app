from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from dependencies.auth import get_current_active_user
from models.user_model import User
from schemas.dashboard import DashboardResponse
from services.dashboard_service import get_dashboard_summary

router = APIRouter()


@router.get("/", response_model=DashboardResponse)
def read_dashboard_summary(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> DashboardResponse:
    """Retorna os dados consolidados do dashboard."""
    return get_dashboard_summary(db)
