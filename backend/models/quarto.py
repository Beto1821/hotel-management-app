"""Modelo ORM para os quartos do hotel."""

from __future__ import annotations

from typing import ClassVar, List, Optional, TYPE_CHECKING

from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:  # pragma: no cover - usado apenas para type checking
    from models.reserva import Reserva


class Quarto(Base):
    """Representa um quarto disponível para reserva."""

    __tablename__: ClassVar[str] = "quartos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    numero: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    tipo: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(20), default="disponivel")
    capacidade: Mapped[int] = mapped_column(Integer, default=1)
    valor_diaria: Mapped[float] = mapped_column(Float, nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    reservas: Mapped[List["Reserva"]] = relationship(
        "Reserva", back_populates="quarto", cascade="all, delete-orphan"
    )


__all__ = ["Quarto"]
