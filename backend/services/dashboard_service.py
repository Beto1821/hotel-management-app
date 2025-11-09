from datetime import date, datetime

from sqlalchemy import distinct, func
from sqlalchemy.orm import Session, selectinload

from models.reserva import Reserva
from models.client_model import Client
from models.quarto import Quarto
from schemas.dashboard import (
    DashboardActivity,
    DashboardResponse,
    DashboardStats,
)
from services.reserva_service import (
    STATUS_ATIVA,
    STATUS_CANCELADA,
    STATUS_CONCLUIDA,
    STATUS_EQUIVALENTS,
    STATUS_PENDENTE,
)


def _get_next_month_start(first_day: date) -> date:
    if first_day.month == 12:
        return date(first_day.year + 1, 1, 1)
    return date(first_day.year, first_day.month + 1, 1)


def get_dashboard_summary(db: Session) -> DashboardResponse:
    today = date.today()
    first_day = today.replace(day=1)
    next_month = _get_next_month_start(first_day)

    total_clients = db.query(func.count(Client.id)).scalar() or 0
    total_rooms = db.query(func.count(Quarto.id)).scalar() or 0

    active_reservas = (
        db.query(func.count(Reserva.id))
        .filter(
            Reserva.status.notin_(
                tuple(STATUS_EQUIVALENTS[STATUS_CANCELADA])
            ),
            Reserva.data_checkout >= today,
        )
        .scalar()
        or 0
    )

    occupied_rooms = (
        db.query(func.count(distinct(Reserva.quarto_id)))
        .filter(
            Reserva.status.notin_(
                tuple(STATUS_EQUIVALENTS[STATUS_CANCELADA])
            ),
            Reserva.data_checkin <= today,
            Reserva.data_checkout > today,
        )
        .scalar()
        or 0
    )

    monthly_revenue = (
        db.query(func.coalesce(func.sum(Reserva.valor_total), 0.0))
        .filter(
            Reserva.status.notin_(
                tuple(STATUS_EQUIVALENTS[STATUS_CANCELADA])
            ),
            Reserva.data_checkin >= first_day,
            Reserva.data_checkin < next_month,
        )
        .scalar()
        or 0.0
    )

    recent_reservas = (
        db.query(Reserva)
        .order_by(Reserva.created_at.desc())
        .options(
            selectinload(Reserva.client),
            selectinload(Reserva.quarto),
        )
        .limit(10)
        .all()
    )

    activities = []
    for reserva in recent_reservas:
        status = reserva.status or "desconhecido"
        status = {
            "confirmado": STATUS_PENDENTE,
            "confirmada": STATUS_PENDENTE,
            "cancelado": STATUS_CANCELADA,
            "cancelada": STATUS_CANCELADA,
            "concluido": STATUS_CONCLUIDA,
            "concluida": STATUS_CONCLUIDA,
            "ativa": STATUS_ATIVA,
        }.get(status, status)
        event_type = (
            "reserva_cancelada"
            if status == STATUS_CANCELADA
            else "reserva_confirmada"
        )

        client_name = reserva.client.name if reserva.client else None
        room_number = reserva.quarto.numero if reserva.quarto else None

        details = []
        if client_name:
            details.append(client_name)
        if room_number:
            details.append(f"Quarto {room_number}")
        details_text = (
            " - ".join(details) if details else f"Reserva #{reserva.id}"
        )

        if event_type == "reserva_cancelada":
            description = f"Reserva cancelada • {details_text}"
        else:
            description = f"Reserva confirmada • {details_text}"

        created_at = reserva.created_at
        if created_at is None:
            created_at = datetime.combine(
                reserva.data_checkin,
                datetime.min.time(),
            )

        activities.append(
            DashboardActivity(
                id=reserva.id,
                description=description,
                status=status,
                event_type=event_type,
                created_at=created_at,
            )
        )

    return DashboardResponse(
        stats=DashboardStats(
            total_clients=total_clients,
            active_reservas=active_reservas,
            occupied_rooms=occupied_rooms,
            total_rooms=total_rooms,
            monthly_revenue=float(monthly_revenue),
        ),
        recent_activities=activities,
    )
