from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from schemas.client_schemas import ClientResponse
from schemas.quarto import Quarto


class ReservaBase(BaseModel):
    data_check_in: date = Field(alias="data_checkin")
    data_check_out: date = Field(alias="data_checkout")
    quarto_id: int
    cliente_id: int = Field(alias="client_id")

    model_config = ConfigDict(populate_by_name=True)


class ReservaCreate(ReservaBase):
    pass


class ReservaUpdate(BaseModel):
    data_check_in: Optional[date] = Field(default=None, alias="data_checkin")
    data_check_out: Optional[date] = Field(default=None, alias="data_checkout")
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
