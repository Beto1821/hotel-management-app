from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional

from core.database import get_db
from models.user_model import User
from schemas.user_schema import TokenData

# Configurações JWT (devem ser movidas para um arquivo de configuração)
SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"

# Esquema OAuth2 para Bearer Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Função de dependência para obter o usuário atual a partir do token JWT.
    
    Esta função:
    1. Decodifica o token JWT usando python-jose
    2. Extrai o username do payload
    3. Busca o usuário no banco de dados
    4. Retorna o usuário ou levanta uma exceção de credenciais inválidas
    
    Args:
        token (str): Token JWT Bearer fornecido no header Authorization
        db (Session): Sessão do banco de dados injetada
        
    Returns:
        User: Objeto do usuário autenticado
        
    Raises:
        HTTPException: 401 se as credenciais forem inválidas
    """
    
    # Exceção padrão para credenciais inválidas
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodificar o token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
            
        token_data = TokenData(username=username)
        
    except JWTError:
        raise credentials_exception
    
    # Buscar o usuário no banco de dados
    user = db.query(User).filter(User.username == token_data.username).first()
    
    if user is None:
        raise credentials_exception
        
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Função de dependência para obter o usuário atual ativo.
    
    Esta função pode ser estendida para verificar se o usuário está ativo,
    não foi banido, tem permissões específicas, etc.
    
    Args:
        current_user (User): Usuário atual obtido via get_current_user
        
    Returns:
        User: Usuário ativo autenticado
        
    Raises:
        HTTPException: 400 se o usuário estiver inativo
    """
    
    # Por enquanto, apenas retorna o usuário
    # Aqui você pode adicionar verificações como:
    # - if not current_user.is_active: raise HTTPException(...)
    # - if current_user.is_banned: raise HTTPException(...)
    
    return current_user
