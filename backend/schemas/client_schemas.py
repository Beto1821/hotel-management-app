"""
Schemas Pydantic para Cliente
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class ClientBase(BaseModel):
    """Schema base para Cliente"""
    name: str
    email: EmailStr
    phone: str
    document: str
    address: Optional[str] = None


class ClientCreate(ClientBase):
    """Schema para criação de Cliente"""
    pass


class ClientUpdate(BaseModel):
    """Schema para atualização de Cliente"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    document: Optional[str] = None
    address: Optional[str] = None


class ClientResponse(ClientBase):
    """Schema de resposta para Cliente"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True
        from_attributes = True