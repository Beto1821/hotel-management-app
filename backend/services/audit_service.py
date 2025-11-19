"""
Serviço para registro de auditoria de ações do sistema
"""
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from models.audit_log import AuditLog


class AuditService:
    """Serviço para registrar ações de auditoria"""
    
    @staticmethod
    def log_action(
        db: Session,
        user_id: int,
        action: str,
        resource: str,
        resource_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[dict] = None
    ) -> AuditLog:
        """
        Registra uma ação de auditoria.
        
        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário que executou a ação
            action: Tipo de ação (LOGIN, LOGOUT, CREATE, UPDATE, DELETE, etc.)
            resource: Tipo de recurso afetado (USER, ROOM, RESERVATION, CLIENT, etc.)
            resource_id: ID do recurso afetado (opcional)
            ip_address: Endereço IP do usuário
            user_agent: User agent do navegador
            details: Informações adicionais em formato JSON
            
        Returns:
            AuditLog: Registro de auditoria criado
        """
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details,
            timestamp=datetime.utcnow()
        )
        
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        
        return audit_log
    
    @staticmethod
    def log_login(
        db: Session,
        user_id: int,
        success: bool,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[dict] = None
    ) -> AuditLog:
        """
        Registra tentativa de login.
        
        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário
            success: Se o login foi bem-sucedido
            ip_address: IP do usuário
            user_agent: User agent do navegador
            details: Detalhes adicionais
            
        Returns:
            AuditLog: Registro de auditoria
        """
        action = "LOGIN_SUCCESS" if success else "LOGIN_FAILED"
        return AuditService.log_action(
            db=db,
            user_id=user_id,
            action=action,
            resource="AUTH",
            ip_address=ip_address,
            user_agent=user_agent,
            details=details
        )
    
    @staticmethod
    def log_logout(
        db: Session,
        user_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        """Registra logout de usuário"""
        return AuditService.log_action(
            db=db,
            user_id=user_id,
            action="LOGOUT",
            resource="AUTH",
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    @staticmethod
    def log_create(
        db: Session,
        user_id: int,
        resource: str,
        resource_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[dict] = None
    ) -> AuditLog:
        """Registra criação de recurso"""
        return AuditService.log_action(
            db=db,
            user_id=user_id,
            action="CREATE",
            resource=resource,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details
        )
    
    @staticmethod
    def log_update(
        db: Session,
        user_id: int,
        resource: str,
        resource_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[dict] = None
    ) -> AuditLog:
        """Registra atualização de recurso"""
        return AuditService.log_action(
            db=db,
            user_id=user_id,
            action="UPDATE",
            resource=resource,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details
        )
    
    @staticmethod
    def log_delete(
        db: Session,
        user_id: int,
        resource: str,
        resource_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[dict] = None
    ) -> AuditLog:
        """Registra exclusão de recurso"""
        return AuditService.log_action(
            db=db,
            user_id=user_id,
            action="DELETE",
            resource=resource,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details
        )
    
    @staticmethod
    def log_password_reset_request(
        db: Session,
        user_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        """Registra solicitação de reset de senha"""
        return AuditService.log_action(
            db=db,
            user_id=user_id,
            action="PASSWORD_RESET_REQUEST",
            resource="AUTH",
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    @staticmethod
    def log_password_reset_complete(
        db: Session,
        user_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        """Registra conclusão de reset de senha"""
        return AuditService.log_action(
            db=db,
            user_id=user_id,
            action="PASSWORD_RESET_COMPLETE",
            resource="AUTH",
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    @staticmethod
    def log_2fa_enabled(
        db: Session,
        user_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        """Registra habilitação de 2FA"""
        return AuditService.log_action(
            db=db,
            user_id=user_id,
            action="2FA_ENABLED",
            resource="AUTH",
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    @staticmethod
    def log_2fa_disabled(
        db: Session,
        user_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        """Registra desabilitação de 2FA"""
        return AuditService.log_action(
            db=db,
            user_id=user_id,
            action="2FA_DISABLED",
            resource="AUTH",
            ip_address=ip_address,
            user_agent=user_agent
        )
