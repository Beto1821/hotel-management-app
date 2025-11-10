import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from models.base import Base


# URL do banco de dados. Pode ser sobrescrita pela variável de ambiente DATABASE_URL
# Exemplo MySQL: "mysql+pymysql://usuario:senha@localhost:3306/hotel_app"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
def _engine_options(url: str) -> dict:
    if url.startswith("sqlite"):
        return {"connect_args": {"check_same_thread": False}}
    return {"pool_pre_ping": True}


SQLALCHEMY_DATABASE_URL = DATABASE_URL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    **_engine_options(SQLALCHEMY_DATABASE_URL),
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
