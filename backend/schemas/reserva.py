from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from schemas.client_schemas import ClientResponse
from schemas.quarto import Quarto


class ReservaBase(BaseModel):
    data_checkin: date
    data_checkout: date
    quarto_id: int
    client_id: int

    model_config = ConfigDict(populate_by_name=True)


class ReservaCreate(ReservaBase):
    pass


class ReservaUpdate(BaseModel):
    data_checkin: Optional[date] = None
    data_checkout: Optional[date] = None
    status: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class Reserva(ReservaBase):
    id: int
    valor_total: float
    status: str
    quarto: Optional[Quarto] = None
    cliente: Optional[ClientResponse] = Field(default=None, alias="client")
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
