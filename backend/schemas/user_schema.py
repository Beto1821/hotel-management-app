from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    """
    Schema base para usuários contendo apenas o username.
    """
    username: str


class UserCreate(UserBase):
    """
    Schema para criação de usuários.
    Herda de UserBase e adiciona o campo password.
    """
    password: str


class User(UserBase):
    """
    Schema para resposta de usuário.
    Herda de UserBase e adiciona o campo id.
    """
    id: int
    
    model_config = {"from_attributes": True}


class Token(BaseModel):
    """
    Schema para resposta de token de autenticação.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema para dados do token JWT.
    """
    username: Optional[str] = None
