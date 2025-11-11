import os
from typing import Generator
from urllib.parse import quote
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from models.base import Base

# Carregar variáveis do arquivo .env
load_dotenv()


# Construir URL do banco de dados usando variáveis separadas
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "password")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "3306")
db_name = os.getenv("DB_NAME", "HOTEL_APP")

# Codificar a senha para URL (necessário se contém caracteres especiais como @)
encoded_password = quote(db_password, safe="")

# Construir a URL sempre a partir das variáveis individuais para evitar problemas de codificação
DATABASE_URL = f"mysql+pymysql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"

# Opções de conexão com base no tipo de banco
def _engine_options(url: str) -> dict:
    if url and url.startswith("sqlite"):
        return {"connect_args": {"check_same_thread": False}}
    return {"pool_pre_ping": True}

# Configuração do banco de dados    
engine = create_engine(
    DATABASE_URL,
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
