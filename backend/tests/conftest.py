import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from models.base import Base
from core.database import get_db

# Configuração do banco de dados de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria as tabelas no banco de dados de teste
Base.metadata.create_all(bind=engine)


def override_get_db():
    """
    Sobrescreve a dependência get_db para usar o banco de dados de teste.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Aplica a sobrescrita da dependência na aplicação
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    """
    Fixture do pytest para fornecer uma sessão de banco de dados de teste.
    Limpa o banco de dados após cada teste.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def test_client():
    """
    Fixture do pytest para fornecer um cliente de teste para a API.
    """
    with TestClient(app) as client:
        yield client
