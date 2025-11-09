from datetime import datetime
from typing import List

from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_clients: int
    active_reservas: int
    occupied_rooms: int
    total_rooms: int
    monthly_revenue: float


class DashboardActivity(BaseModel):
    id: int
    description: str
    status: str
    event_type: str
    created_at: datetime


class DashboardResponse(BaseModel):
    stats: DashboardStats
    recent_activities: List[DashboardActivity]
