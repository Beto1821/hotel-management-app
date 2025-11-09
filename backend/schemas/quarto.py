"""Schemas Pydantic para recursos de quartos."""

from typing import Optional

from pydantic import BaseModel, ConfigDict

class QuartoBase(BaseModel):
    numero: str
    tipo: str
    status: str
    capacidade: int
    valor_diaria: float
    descricao: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class QuartoCreate(QuartoBase):
    pass


class QuartoUpdate(BaseModel):
    numero: Optional[str] = None
    tipo: Optional[str] = None
    status: Optional[str] = None
    capacidade: Optional[int] = None
    valor_diaria: Optional[float] = None
    descricao: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class Quarto(QuartoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
