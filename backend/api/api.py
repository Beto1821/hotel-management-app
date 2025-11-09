from fastapi import APIRouter

from api.endpoints.auth import router as auth_router
from api.endpoints.clients import router as clients_router
from api.endpoints.reservas import router as reservas_router
from api.endpoints.quartos import router as quartos_router

# Criar router principal da API
api_router = APIRouter()

# Incluir rotas de autenticação
api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"]
)

# Incluir rotas de clientes
api_router.include_router(
    clients_router,
    prefix="/clients",
    tags=["clients"]
)

# Incluir rotas de reservas
api_router.include_router(
    reservas_router,
    prefix="/reservas",
    tags=["reservas"],
)

# Incluir rotas de quartos
api_router.include_router(
    quartos_router,
    prefix="/quartos",
    tags=["quartos"],
)
