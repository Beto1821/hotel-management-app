"""Schemas Pydantic para recursos de quartos."""

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class QuartoBase(BaseModel):
    numero: str
    tipo: str
    capacidade: int = 1
    valor_diaria: float
    status: str = "disponivel"
    descricao: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class QuartoCreate(QuartoBase):
    pass


class QuartoUpdate(BaseModel):
    numero: Optional[str] = None
    tipo: Optional[str] = None
    capacidade: Optional[int] = None
    valor_diaria: Optional[float] = None
    status: Optional[str] = None
    descricao: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class Quarto(QuartoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class QuartoCalendarDay(BaseModel):
    data: date
    status: str
    reserva_id: Optional[int] = None
    reserva_status: Optional[str] = None
    cliente_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class QuartoCalendar(BaseModel):
    quarto_id: int
    numero: str
    tipo: str
    status: str
    capacidade: int
    valor_diaria: float
    periodo_inicio: date
    periodo_fim: date
    ocupacao: List[QuartoCalendarDay]

    model_config = ConfigDict(from_attributes=True)
