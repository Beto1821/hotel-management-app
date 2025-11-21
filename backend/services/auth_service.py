import bcrypt
from typing import Optional
import re
import pyotp
import secrets
from datetime import datetime, timedelta
from jose import jwt

from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def get_password_hash(password: str) -> str:
    """
    Gera o hash da senha usando bcrypt.

    Args:
        password (str): Senha em texto plano

    Returns:
        str: Senha hasheada
    """
    # Bcrypt limita senhas a 72 bytes
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha em texto plano corresponde ao hash armazenado.

    Args:
        plain_password (str): Senha em texto plano fornecida pelo usuário
        hashed_password (str): Hash da senha armazenado no banco de dados

    Returns:
        bool: True se as senhas coincidirem, False caso contrário
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """
    Esqueleto da função de autenticação de usuário.

    Esta função deve:
    1. Buscar o usuário no banco de dados pelo username
    2. Verificar se a senha está correta usando verify_password
    3. Retornar os dados do usuário se autenticado com sucesso

    Args:
        username (str): Nome de usuário
        password (str): Senha em texto plano

    Returns:
        Optional[dict]: Dados do usuário se autenticado, None caso contrário
    """
    # TODO: Implementar a lógica de busca no banco de dados
    # TODO: Usar verify_password para validar a senha
    # TODO: Retornar dados do usuário ou None
    pass


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Valida a força de uma senha.
    
    Requisitos:
    - Mínimo 8 caracteres
    - Pelo menos uma letra maiúscula
    - Pelo menos uma letra minúscula
    - Pelo menos um número
    - Pelo menos um caractere especial
    
    Args:
        password (str): Senha para validar
        
    Returns:
        tuple[bool, str]: (True se válida, mensagem de erro ou sucesso)
    """
    if len(password) < 8:
        return False, "A senha deve ter no mínimo 8 caracteres"
    
    if not re.search(r"[A-Z]", password):
        return False, "A senha deve conter pelo menos uma letra maiúscula"
    
    if not re.search(r"[a-z]", password):
        return False, "A senha deve conter pelo menos uma letra minúscula"
    
    if not re.search(r"\d", password):
        return False, "A senha deve conter pelo menos um número"
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "A senha deve conter pelo menos um caractere especial"
    
    return True, "Senha válida"


def generate_2fa_secret() -> str:
    """
    Gera um secret para autenticação de dois fatores (TOTP).
    
    Returns:
        str: Secret base32 para TOTP
    """
    return pyotp.random_base32()


def generate_2fa_qr_uri(
    secret: str,
    username: str,
    issuer: str = "Hotel App"
) -> str:
    """
    Gera URI para QR Code de configuração do 2FA.
    
    Args:
        secret (str): Secret TOTP do usuário
        username (str): Nome de usuário
        issuer (str): Nome da aplicação
        
    Returns:
        str: URI otpauth para gerar QR Code
    """
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=username, issuer_name=issuer)


def verify_2fa_token(secret: str, token: str) -> bool:
    """
    Verifica um token 2FA.
    
    Args:
        secret (str): Secret TOTP do usuário
        token (str): Token de 6 dígitos fornecido
        
    Returns:
        bool: True se o token é válido
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(token, valid_window=1)  # Aceita tokens 30s antes/depois


def generate_reset_token() -> str:
    """
    Gera um token seguro para reset de senha.
    
    Returns:
        str: Token aleatório de 32 bytes em hexadecimal
    """
    return secrets.token_urlsafe(32)


def is_account_locked(
    failed_attempts: int,
    locked_until: Optional[datetime]
) -> bool:
    """
    Verifica se uma conta está bloqueada por tentativas de login falhadas.
    
    Args:
        failed_attempts (int): Número de tentativas falhadas
        locked_until (Optional[datetime]): Data/hora até quando a conta
            está bloqueada
        
    Returns:
        bool: True se a conta está bloqueada
    """
    # Bloqueia após 5 tentativas falhadas
    if failed_attempts >= 5:
        # Se não tem locked_until definido, está bloqueado
        # permanentemente até reset
        if locked_until is None:
            return True
        # Se tem locked_until, verifica se ainda está dentro do
        # período de bloqueio
        if datetime.utcnow() < locked_until:
            return True
    
    return False


def calculate_lockout_time(failed_attempts: int) -> Optional[datetime]:
    """
    Calcula o tempo de bloqueio baseado no número de tentativas falhadas.
    
    Args:
        failed_attempts (int): Número de tentativas falhadas
        
    Returns:
        Optional[datetime]: Data/hora até quando bloquear, ou None se
            não bloquear
    """
    if failed_attempts >= 5:
        # Bloqueio progressivo: 15 min, 30 min, 1h, 2h, 4h...
        lockout_minutes = 15 * (2 ** (failed_attempts - 5))
        # Máximo de 24 horas
        lockout_minutes = min(lockout_minutes, 24 * 60)
        return datetime.utcnow() + timedelta(minutes=lockout_minutes)
    
    return None


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Cria um token JWT de acesso.

    Args:
        data (dict): Dados para incluir no token (ex: {"sub": username})
        expires_delta (Optional[timedelta]): Tempo de expiração do token

    Returns:
        str: Token JWT codificado
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
