"""Modelo ORM para representar as reservas de hospedagem."""

from __future__ import annotations

from datetime import date, datetime
from typing import ClassVar, Optional, TYPE_CHECKING

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.client_model import Client
    from models.quarto import Quarto


class Reserva(Base):
    """Representa a reserva de um quarto por um cliente."""

    __tablename__: ClassVar[str] = "reservas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    data_checkin: Mapped[date] = mapped_column(Date, nullable=False)
    data_checkout: Mapped[date] = mapped_column(Date, nullable=False)
    valor_total: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String, default="pendente")

    quarto_id: Mapped[int] = mapped_column(
        ForeignKey("quartos.id"), nullable=False
    )
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"), nullable=False
    )

    quarto: Mapped["Quarto"] = relationship(
        "Quarto", back_populates="reservas"
    )
    client: Mapped["Client"] = relationship(
        "Client", back_populates="reservas"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )


__all__ = ["Reserva"]
