from passlib.context import CryptContext
from typing import Optional

# Configuração do contexto de criptografia usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Gera o hash da senha usando bcrypt.

    Args:
        password (str): Senha em texto plano

    Returns:
        str: Senha hasheada
    """
    truncated_password = password.encode('utf-8')[:72]
    return pwd_context.hash(truncated_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha em texto plano corresponde ao hash armazenado.

    Args:
        plain_password (str): Senha em texto plano fornecida pelo usuário
        hashed_password (str): Hash da senha armazenado no banco de dados

    Returns:
        bool: True se as senhas coincidirem, False caso contrário
    """
    truncated_plain_password = plain_password.encode('utf-8')[:72]
    return pwd_context.verify(truncated_plain_password, hashed_password)


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


def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    """
    Esqueleto da função para criação de token JWT.

    Esta função deve:
    1. Criar um payload JWT com os dados fornecidos
    2. Definir tempo de expiração do token
    3. Codificar e retornar o token JWT

    Args:
        data (dict): Dados para incluir no token
        expires_delta (Optional[int]): Tempo de expiração em minutos

    Returns:
        str: Token JWT codificado
    """
    # TODO: Implementar criação de token JWT
    # TODO: Usar python-jose para codificação
    # TODO: Definir SECRET_KEY e ALGORITHM
    pass
