from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from core.database import get_db
from models.user_model import User
from schemas.user_schema import UserCreate, User as UserSchema, Token
from services.auth_service import get_password_hash, verify_password

# Criar o router para autenticação
router = APIRouter(tags=["authentication"])

# Configurações JWT (devem ser movidas para um arquivo de configuração)
SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Registrar um novo usuário no sistema.

    Args:
        user_data (UserCreate): Dados do usuário (username e password)
        db (Session): Sessão do banco de dados

    Returns:
        UserSchema: Dados do usuário criado (sem a senha)

    Raises:
        HTTPException: 400 se o username já existir
    """

    # Verificar se o usuário já existe
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Criar hash da senha
    hashed_password = get_password_hash(user_data.password)

    # Criar novo usuário
    db_user = User(
        username=user_data.username,
        hashed_password=hashed_password
    )

    # Salvar no banco de dados
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/token", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Autenticar usuário e retornar token JWT.

    Args:
        form_data (OAuth2PasswordRequestForm): Dados de login (username e password)
        db (Session): Sessão do banco de dados

    Returns:
        Token: Token de acesso JWT e tipo do token

    Raises:
        HTTPException: 401 se as credenciais forem inválidas
    """

    # Buscar usuário no banco de dados
    user = db.query(User).filter(User.username == form_data.username).first()

    # Verificar se o usuário existe e a senha está correta
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
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
