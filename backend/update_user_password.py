#!/usr/bin/env python
"""Script para atualizar a senha do usuário teste."""
import sys
from sqlalchemy.orm import Session

# Importar as configurações
from core.database import SessionLocal
from models.user_model import User
from services.auth_service import get_password_hash


def update_user_password(username: str, new_password: str):
    """Atualiza a senha de um usuário."""
    db = SessionLocal()
    try:
        # Buscar usuário
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            print(f"❌ Usuário '{username}' não encontrado!")
            return False
        
        # Atualizar senha
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        
        print(f"✅ Senha do usuário '{username}' atualizada com sucesso!")
        print(f"📝 Nova senha: {new_password}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar senha: {e}")
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("ATUALIZAR SENHA DO USUÁRIO")
    print("=" * 60)
    
    # Atualizar senha do usuário teste
    update_user_password("teste", "teste123")
    
    print("\n" + "=" * 60)
    print("Agora você pode fazer login com:")
    print("  Username: teste")
    print("  Password: teste123")
    print("=" * 60)
