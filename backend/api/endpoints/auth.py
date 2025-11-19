from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from core.database import get_db
from models.user_model import User, UserRole
from schemas.user_schema import UserCreate, User as UserSchema, Token
from services.auth_service import (
    get_password_hash, 
    verify_password,
    validate_password_strength,
    is_account_locked,
    calculate_lockout_time
)
from services.audit_service import AuditService
from utils.request_utils import get_client_info

# Criar o router para autenticação
router = APIRouter(tags=["authentication"])

# Configurações JWT (devem ser movidas para um arquivo de configuração)
SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Registrar um novo usuário no sistema.

    Args:
        user_data (UserCreate): Dados do usuário (username, email e password)
        request (Request): Requisição HTTP para capturar IP e user agent
        db (Session): Sessão do banco de dados

    Returns:
        UserSchema: Dados do usuário criado (sem a senha)

    Raises:
        HTTPException: 400 se o username já existir ou senha fraca
    """

    # Verificar se o usuário já existe
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Verificar se o email já existe (se fornecido)
    if hasattr(user_data, 'email') and user_data.email:
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Validar força da senha
    is_valid, message = validate_password_strength(user_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    # Criar hash da senha
    hashed_password = get_password_hash(user_data.password)

    # Criar novo usuário com role padrão VIEWER
    db_user = User(
        username=user_data.username,
        email=user_data.email if hasattr(user_data, 'email') else None,
        hashed_password=hashed_password,
        role=UserRole.VIEWER,  # Novos usuários começam como VIEWER
        is_active=True
    )

    # Salvar no banco de dados
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Registrar auditoria
    client_info = get_client_info(request)
    AuditService.log_action(
        db=db,
        user_id=db_user.id,
        action="USER_CREATED",
        resource="USER",
        resource_id=db_user.id,
        ip_address=client_info["ip_address"],
        user_agent=client_info["user_agent"]
    )

    return db_user


@router.post("/token", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None,
    db: Session = Depends(get_db)
):
    """
    Autenticar usuário e retornar token JWT.
    
    Implementa proteções de segurança:
    - Verificação de conta bloqueada
    - Contador de tentativas falhadas
    - Bloqueio progressivo após múltiplas falhas
    - Registro de auditoria
    - Atualização de last_login

    Args:
        form_data (OAuth2PasswordRequestForm): Dados de login (username e password)
        request (Request): Requisição HTTP para capturar IP e user agent
        db (Session): Sessão do banco de dados

    Returns:
        Token: Token de acesso JWT e tipo do token

    Raises:
        HTTPException: 401 se as credenciais forem inválidas
        HTTPException: 403 se a conta estiver bloqueada
    """
    
    # Obter informações do cliente
    client_info = get_client_info(request) if request else {"ip_address": None, "user_agent": None}

    # Buscar usuário no banco de dados
    user = db.query(User).filter(User.username == form_data.username).first()

    # Se usuário não existe, retorna erro genérico (não revela se username existe)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar se a conta está bloqueada
    if is_account_locked(user.failed_login_attempts, user.locked_until):
        # Registrar tentativa de login em conta bloqueada
        AuditService.log_login(
            db=db,
            user_id=user.id,
            success=False,
            ip_address=client_info["ip_address"],
            user_agent=client_info["user_agent"],
            details={"reason": "account_locked"}
        )
        
        lockout_message = "Conta bloqueada devido a múltiplas tentativas de login falhadas."
        if user.locked_until:
            lockout_message += f" Tente novamente após {user.locked_until.strftime('%d/%m/%Y %H:%M:%S')}"
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=lockout_message,
        )
    
    # Verificar se o usuário está ativo
    if not user.is_active:
        AuditService.log_login(
            db=db,
            user_id=user.id,
            success=False,
            ip_address=client_info["ip_address"],
            user_agent=client_info["user_agent"],
            details={"reason": "account_inactive"}
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta inativa. Contate o administrador.",
        )

    # Verificar senha
    if not verify_password(form_data.password, user.hashed_password):
        # Incrementar contador de tentativas falhadas
        user.failed_login_attempts += 1
        user.locked_until = calculate_lockout_time(user.failed_login_attempts)
        db.commit()
        
        # Registrar tentativa falhada
        AuditService.log_login(
            db=db,
            user_id=user.id,
            success=False,
            ip_address=client_info["ip_address"],
            user_agent=client_info["user_agent"],
            details={
                "reason": "invalid_password",
                "failed_attempts": user.failed_login_attempts
            }
        )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Login bem-sucedido - resetar contador de falhas
    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_login = datetime.utcnow()
    user.last_login_ip = client_info["ip_address"]
    db.commit()
    
    # Registrar login bem-sucedido
    AuditService.log_login(
        db=db,
        user_id=user.id,
        success=True,
        ip_address=client_info["ip_address"],
        user_agent=client_info["user_agent"]
    )

    # Criar token de acesso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Criar token JWT de acesso.

    Args:
        data (dict): Dados para incluir no token
        expires_delta (timedelta): Tempo de expiração do token

    Returns:
        str: Token JWT codificado
    """
    from jose import jwt

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


@router.post("/forgot-password")
def forgot_password(
    username: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Solicita reset de senha.
    
    Gera um token de reset que expira em 1 hora.
    Em produção, envie este token por email.
    
    Args:
        username: Nome de usuário ou email
        request: Requisição HTTP
        db: Sessão do banco de dados
        
    Returns:
        dict: Mensagem de sucesso e token (em produção, enviar apenas por email)
    """
    from services.auth_service import generate_reset_token
    
    # Buscar usuário por username ou email
    user = db.query(User).filter(
        (User.username == username) | (User.email == username)
    ).first()
    
    # Por segurança, sempre retorna sucesso mesmo se usuário não existir
    # Isso evita enumerar usuários válidos
    if not user:
        return {
            "message": "Se o usuário existir, um email será enviado com instruções para reset de senha."
        }
    
    # Gerar token de reset
    reset_token = generate_reset_token()
    user.reset_token = reset_token
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
    db.commit()
    
    # Obter informações do cliente
    client_info = get_client_info(request)
    
    # Registrar auditoria
    AuditService.log_password_reset_request(
        db=db,
        user_id=user.id,
        ip_address=client_info["ip_address"],
        user_agent=client_info["user_agent"]
    )
    
    # TODO: Em produção, enviar email com o link de reset
    # send_password_reset_email(user.email, reset_token)
    
    # Por enquanto, retorna o token (APENAS PARA DESENVOLVIMENTO)
    return {
        "message": "Token de reset gerado com sucesso. Em produção, seria enviado por email.",
        "reset_token": reset_token,  # REMOVER EM PRODUÇÃO
        "expires_at": user.reset_token_expires
    }


@router.post("/reset-password")
def reset_password(
    token: str,
    new_password: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Reseta a senha usando o token de reset.
    
    Args:
        token: Token de reset gerado em forgot-password
        new_password: Nova senha
        request: Requisição HTTP
        db: Sessão do banco de dados
        
    Returns:
        dict: Mensagem de sucesso
        
    Raises:
        HTTPException: 400 se token inválido ou expirado, ou senha fraca
    """
    from services.auth_service import validate_password_strength
    
    # Buscar usuário com o token
    user = db.query(User).filter(User.reset_token == token).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de reset inválido"
        )
    
    # Verificar se o token expirou
    if not user.reset_token_expires or user.reset_token_expires < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de reset expirado. Solicite um novo token."
        )
    
    # Validar força da nova senha
    is_valid, message = validate_password_strength(new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    # Atualizar senha
    user.hashed_password = get_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expires = None
    user.failed_login_attempts = 0  # Resetar contador de falhas
    user.locked_until = None  # Desbloquear conta se estiver bloqueada
    db.commit()
    
    # Obter informações do cliente
    client_info = get_client_info(request)
    
    # Registrar auditoria
    AuditService.log_password_reset_complete(
        db=db,
        user_id=user.id,
        ip_address=client_info["ip_address"],
        user_agent=client_info["user_agent"]
    )
    
    return {
        "message": "Senha resetada com sucesso. Você já pode fazer login com a nova senha."
    }
