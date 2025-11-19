"""
Dependências para controle de permissões baseado em roles
"""
from fastapi import Depends, HTTPException, status
from models.user_model import User, UserRole
from dependencies.auth import get_current_active_user


def require_role(*allowed_roles: UserRole):
    """
    Decorator factory para verificar se o usuário tem uma das roles permitidas
    
    Args:
        *allowed_roles: Roles permitidas para acessar o endpoint
        
    Returns:
        Função de dependência que verifica a role do usuário
        
    Raises:
        HTTPException 403: Se o usuário não tiver permissão
    """
    def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permissão insuficiente. Requer uma das roles: {', '.join([r.value for r in allowed_roles])}"
            )
        return current_user
    return role_checker


# Aliases para facilitar o uso
require_admin = require_role(UserRole.ADMIN)
require_manager = require_role(UserRole.ADMIN, UserRole.MANAGER)
require_staff = require_role(UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST)
require_any_authenticated = require_role(UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST, UserRole.VIEWER)
