from sqlalchemy import Column, Integer, String
from models.base import Base


class User(Base):
    """
    Modelo SQLAlchemy para representar usuários do sistema.
    
    Attributes:
        id: Chave primária do usuário
        username: Nome de usuário único
        hashed_password: Senha hasheada do usuário
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
