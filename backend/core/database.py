from sqlalchemy import create_engine, text
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
    _apply_sqlite_schema_patches()


def _apply_sqlite_schema_patches():
    """Aplica ajustes pontuais para colunas adicionadas sem migração formal."""
    with engine.begin() as conn:
        columns = {
            row[1]
            for row in conn.execute(text("PRAGMA table_info(quartos)"))
        }

        if "status" not in columns:
            conn.execute(
                text(
                    "ALTER TABLE quartos ADD COLUMN status VARCHAR(50) "
                    "DEFAULT 'disponivel'"
                )
            )
            conn.execute(
                text(
                    "UPDATE quartos SET status = 'disponivel' "
                    "WHERE status IS NULL"
                )
            )

        if "capacidade" not in columns:
            conn.execute(
                text(
                    "ALTER TABLE quartos ADD COLUMN capacidade INTEGER "
                    "DEFAULT 1"
                )
            )
            conn.execute(
                text(
                    "UPDATE quartos SET capacidade = 1 "
                    "WHERE capacidade IS NULL"
                )
            )

        if "valor_diaria" not in columns:
            conn.execute(
                text(
                    "ALTER TABLE quartos ADD COLUMN valor_diaria FLOAT "
                    "DEFAULT 0"
                )
            )
            conn.execute(
                text(
                    "UPDATE quartos SET valor_diaria = 0 "
                    "WHERE valor_diaria IS NULL"
                )
            )

        if "descricao" not in columns:
            conn.execute(
                text(
                    "ALTER TABLE quartos ADD COLUMN descricao TEXT"
                )
            )
