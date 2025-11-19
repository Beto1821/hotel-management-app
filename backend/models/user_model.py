"""Modelo ORM para usuários da aplicação com sistema de roles e segurança."""

from datetime import datetime
from enum import Enum
from typing import ClassVar, Optional

from sqlalchemy import String, Boolean, DateTime, Enum as SQLEnum, Integer
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class UserRole(str, Enum):
    """Roles de usuário do sistema"""
    ADMIN = "admin"
    MANAGER = "manager"
    RECEPTIONIST = "receptionist"
    VIEWER = "viewer"


class User(Base):
    """Representa um usuário autenticável do sistema."""

    __tablename__: ClassVar[str] = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.VIEWER, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # 2FA
    totp_secret: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    is_2fa_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Recuperação de senha
    reset_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    reset_token_expires: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Segurança
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    locked_until: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Auditoria
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_login_ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)

    def __repr__(self):
        return f"<User {self.username} ({self.role.value})>"
