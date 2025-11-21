"""Schemas Pydantic para recursos de quartos."""

from datetime import date
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict


class QuartoBase(BaseModel):
    numero: str
    tipo: Literal["standard", "deluxe", "suite"]
    capacidade: int = 1
    valor_diaria: float
    status: Literal["livre", "ocupado", "limpeza", "manutencao"] = "livre"
    descricao: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class QuartoCreate(QuartoBase):
    pass


class QuartoUpdate(BaseModel):
    numero: Optional[str] = None
    tipo: Optional[Literal["standard", "deluxe", "suite"]] = None
    capacidade: Optional[int] = None
    valor_diaria: Optional[float] = None
    status: Optional[
        Literal["livre", "ocupado", "limpeza", "manutencao"]
    ] = None
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
