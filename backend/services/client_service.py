"""
Serviços para gerenciamento de Clientes
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.client_model import Client
from schemas.client_schemas import ClientCreate, ClientUpdate


class ClientService:
    """Serviço para operações CRUD de clientes"""
    
    @staticmethod
    def create_client(db: Session, client_data: ClientCreate) -> Client:
        """
        Cria um novo cliente
        """
        try:
            db_client = Client(
                name=client_data.name,
                email=client_data.email,
                phone=client_data.phone,
                document=client_data.document,
                address=client_data.address
            )
            db.add(db_client)
            db.commit()
            db.refresh(db_client)
            return db_client
        except IntegrityError:
            db.rollback()
            raise ValueError("Email ou documento já cadastrado")
    
    @staticmethod
    def get_client(db: Session, client_id: int) -> Optional[Client]:
        """
        Busca um cliente por ID
        """
        return db.query(Client).filter(Client.id == client_id).first()
    
    @staticmethod
    def get_client_by_email(db: Session, email: str) -> Optional[Client]:
        """
        Busca um cliente por email
        """
        return db.query(Client).filter(Client.email == email).first()
    
    @staticmethod
    def get_client_by_document(db: Session, document: str) -> Optional[Client]:
        """
        Busca um cliente por documento
        """
        return db.query(Client).filter(Client.document == document).first()
    
    @staticmethod
    def get_clients(
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Client]:
        """
        Lista todos os clientes com paginação
        """
        return db.query(Client).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_client(
        db: Session, 
        client_id: int, 
        client_data: ClientUpdate
    ) -> Optional[Client]:
        """
        Atualiza um cliente existente
        """
        db_client = db.query(Client).filter(Client.id == client_id).first()
        if not db_client:
            return None
        
        # Atualizar apenas campos fornecidos
        update_data = client_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_client, field, value)
        
        try:
            db.commit()
            db.refresh(db_client)
            return db_client
        except IntegrityError:
            db.rollback()
            raise ValueError("Email ou documento já cadastrado")
    
    @staticmethod
    def delete_client(db: Session, client_id: int) -> bool:
        """
        Remove um cliente
        """
        db_client = db.query(Client).filter(Client.id == client_id).first()
        if not db_client:
            return False
        
        db.delete(db_client)
        db.commit()
        return True
    
    @staticmethod
    def search_clients(
        db: Session, 
        query: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Client]:
        """
        Busca clientes por nome ou email
        """
        return (
            db.query(Client)
            .filter(
                (Client.name.ilike(f"%{query}%")) | 
                (Client.email.ilike(f"%{query}%"))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )