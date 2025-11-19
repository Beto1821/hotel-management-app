"""
Modelo de auditoria para log de ações do sistema
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from models.base import Base


class AuditLog(Base):
    """Log de auditoria para rastrear ações dos usuários"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)  # LOGIN, LOGOUT, CREATE_ROOM, etc
    resource = Column(String(100), nullable=True)  # quartos, reservas, clientes, etc
    resource_id = Column(Integer, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    details = Column(Text, nullable=True)  # JSON com detalhes adicionais
    
    def __repr__(self):
        return f"<AuditLog {self.action} by user {self.user_id} at {self.timestamp}>"
