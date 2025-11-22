#!/usr/bin/env python3
"""Script para criar um usuário de teste local"""
import os
import bcrypt
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from urllib.parse import quote

# Carregar variáveis de ambiente
load_dotenv()

# Dados do novo usuário
USERNAME = "teste"
PASSWORD = "Teste123!"
EMAIL = "teste@hotel.com"
ROLE = "ADMIN"

# Gerar hash da senha
hashed_password = bcrypt.hashpw(PASSWORD.encode('utf-8'), bcrypt.gensalt())
hashed_password_str = hashed_password.decode('utf-8')

print("🔐 Criando usuário de teste...")
print(f"Username: {USERNAME}")
print(f"Password: {PASSWORD}")
print(f"Email: {EMAIL}")
print(f"Role: {ROLE}")
print(f"\nHash gerado: {hashed_password_str}\n")

# Construir URL do banco de dados
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "password")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "3306")
db_name = os.getenv("DB_NAME", "HOTEL_APP")

encoded_password = quote(db_password, safe="")
DATABASE_URL = f"mysql+pymysql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Verificar se o usuário já existe
        result = conn.execute(
            text("SELECT id FROM users WHERE username = :username OR email = :email"),
            {"username": USERNAME, "email": EMAIL}
        )
        existing_user = result.fetchone()
        
        if existing_user:
            print(f"⚠️  Usuário já existe! Atualizando senha...")
            conn.execute(
                text("""
                    UPDATE users 
                    SET hashed_password = :password,
                        updated_at = NOW()
                    WHERE username = :username
                """),
                {"password": hashed_password_str, "username": USERNAME}
            )
            conn.commit()
            print("✅ Senha atualizada com sucesso!")
        else:
            print(f"➕ Criando novo usuário...")
            conn.execute(
                text("""
                    INSERT INTO users (username, email, hashed_password, role, is_active, created_at, updated_at)
                    VALUES (:username, :email, :password, :role, 1, NOW(), NOW())
                """),
                {
                    "username": USERNAME,
                    "email": EMAIL,
                    "password": hashed_password_str,
                    "role": ROLE
                }
            )
            conn.commit()
            print("✅ Usuário criado com sucesso!")
        
        print("\n" + "="*50)
        print("📋 CREDENCIAIS DE TESTE:")
        print("="*50)
        print(f"Username: {USERNAME}")
        print(f"Password: {PASSWORD}")
        print(f"Email: {EMAIL}")
        print(f"Role: {ROLE}")
        print("="*50)
        
except Exception as e:
    print(f"❌ Erro ao criar usuário: {e}")
finally:
    engine.dispose()
