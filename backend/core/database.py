from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from models.base import Base

# URL do banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# Criar engine do SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Necessário para SQLite
)

# Criar SessionLocal para criar sessões do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Função de dependência para injetar sessões do banco de dados no FastAPI.
    
    Yields:
        Session: Sessão do banco de dados SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Criar todas as tabelas no banco de dados.
    Esta função deve ser chamada na inicialização da aplicação.
    """
    Base.metadata.create_all(bind=engine)
