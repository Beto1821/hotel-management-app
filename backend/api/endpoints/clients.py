"""
Endpoints da API para gerenciamento de Clientes
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from core.database import get_db
from dependencies.auth import get_current_user
from models.user_model import User
from schemas.client_schemas import (
    ClientCreate,
    ClientUpdate,
    ClientResponse
)
from services.client_service import ClientService
from services.audit_service import AuditService
from utils.request_utils import get_client_info

# Router para clientes
router = APIRouter(
    # prefix="/clients",
    tags=["clients"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=ClientResponse,
             status_code=status.HTTP_201_CREATED)
async def create_client(
    client_data: ClientCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cria um novo cliente
    """
    try:
        client = ClientService.create_client(db, client_data)
        
        # Registrar auditoria
        client_info = get_client_info(request)
        AuditService.log_action(
            db=db,
            user_id=current_user.id,
            action="CREATE_CLIENT",
            resource="CLIENT",
            resource_id=client.id,
            ip_address=client_info["ip_address"],
            user_agent=client_info["user_agent"],
            details={"client_name": client.nome}
        )
        
        return client
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[ClientResponse])
async def list_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista todos os clientes com paginação
    """
    clients = ClientService.get_clients(db, skip=skip, limit=limit)
    return clients


@router.get("/search", response_model=List[ClientResponse])
async def search_clients(
    q: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Busca clientes por nome ou email
    """
    clients = ClientService.search_clients(db, q, skip=skip, limit=limit)
    return clients


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Busca um cliente específico por ID
    """
    client = ClientService.get_client(db, client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    return client


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client_data: ClientUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza um cliente existente
    """
    try:
        client = ClientService.update_client(db, client_id, client_data)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )
        
        # Registrar auditoria
        client_info = get_client_info(request)
        AuditService.log_action(
            db=db,
            user_id=current_user.id,
            action="UPDATE_CLIENT",
            resource="CLIENT",
            resource_id=client.id,
            ip_address=client_info["ip_address"],
            user_agent=client_info["user_agent"],
            details={"client_name": client.nome}
        )
        
        return client
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove um cliente
    """
    success = ClientService.delete_client(db, client_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
