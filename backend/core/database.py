import os
from typing import Generator
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from models.base import Base

# Carregar variáveis do arquivo .env
load_dotenv()

# Obter DATABASE_URL do arquivo .env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL não definida! "
        "Adicione DATABASE_URL ao seu arquivo .env "
        "(ex: mysql+pymysql://user:password@localhost:3306/database)"
    )


# Opções de conexão com base no tipo de banco
def _engine_options(url: str) -> dict:
    if url and url.startswith("sqlite"):
        return {"connect_args": {"check_same_thread": False}}
    return {"pool_pre_ping": True}


# Configuração do banco de dados
engine = create_engine(
    DATABASE_URL,
    pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
    **_engine_options(DATABASE_URL),
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
    Criar todas as tabelas no banco de dados configurado.
    Esta função deve ser chamada na inicialização da aplicação.
    """
    Base.metadata.create_all(bind=engine)


# Removido: _apply_sqlite_schema_patches (apenas relevante para SQLite)
