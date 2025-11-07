from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.api import api_router
from core.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de ciclo de vida da aplicação.
    Executa operações de startup e shutdown.
    """
    # Startup: Criar todas as tabelas no banco de dados
    create_tables()
    yield
    # Shutdown: Operações de limpeza (se necessário)


# Criar instância do FastAPI
app = FastAPI(
    title="Hotel Management API",
    description="API para gerenciamento de hotel com autenticação JWT",
    version="1.0.0",
    lifespan=lifespan
)

# Incluir rotas da API
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    """
    Endpoint raiz da API.
    
    Returns:
        dict: Mensagem de boas-vindas
    """
    return {
        "message": "Hotel Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """
    Endpoint de verificação de saúde da API.
    
    Returns:
        dict: Status da aplicação
    """
    return {"status": "healthy", "message": "API is running"}
