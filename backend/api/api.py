from fastapi import APIRouter

from api.endpoints.auth import router as auth_router
from api.endpoints.clients import router as clients_router

# Criar router principal da API
api_router = APIRouter()

# Incluir rotas de autenticação
api_router.include_router(
    auth_router,
    prefix="/v1/auth",
    tags=["auth"]
)

# Incluir rotas de clientes
api_router.include_router(
    clients_router,
    prefix="/v1/clients",
    tags=["clients"]
)
