"""
Modelo de Cliente para o sistema de gerenciamento do hotel
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from models.base import Base


class Client(Base):
    """
    Modelo que representa um cliente do hotel
    """
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    document = Column(String(20), unique=True, nullable=False, index=True)
    address = Column(Text, nullable=True)
    
    # Campos de auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}', email='{self.email}')>"