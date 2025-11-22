#!/usr/bin/env python3
"""Script para verificar a senha do admin"""
import bcrypt

# Hash do banco de dados
stored_hash = "$2b$12$2.A6BVZbT1ZwWxgVJ33o/e2ZFNaG9wVqjvMUpZfb4eFM6gBRC.5w."

# Senhas comuns para testar
passwords_to_test = [
    # Senhas simples
    "admin",
    "admin123",
    "Admin123",
    "Admin123!",
    "password",
    "password123",
    "hotel123",
    "Hotel123!",
    "12345678",
    "admin@hotel",
    # Variações
    "adminadmin",
    "admin1234",
    "Admin1234",
    "Admin@123",
    "Admin#123",
    "hotel",
    "hotel@123",
    "Hotel@123",
    "senha123",
    "Senha123",
    "Senha123!",
    "senha",
    # Mais específicas
    "plataforma",
    "Plataforma123",
    "Plataforma123!",
    "hotelapp",
    "HotelApp123",
    "HotelApp123!",
    # Admin variations
    "administrator",
    "Administrator123",
    "root",
    "root123",
    "Root123!",
    # Comuns em produção
    "123456",
    "qwerty",
    "abc123",
    "Abc123!",
]

print("🔍 Testando senhas comuns...\n")

for password in passwords_to_test:
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        print(f"✅ SENHA ENCONTRADA: '{password}'")
        print(f"\n📋 Credenciais:")
        print(f"   Username: admin")
        print(f"   Password: {password}")
        break
else:
    print("❌ Nenhuma senha comum corresponde ao hash.")
    print("\nVocê pode resetar a senha criando um novo usuário admin:")
    print("\nPython:")
    print(">>> import bcrypt")
    print(">>> senha = 'SuaNovaSenha123!'")
    print(">>> hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())")
    print(">>> print(hash.decode('utf-8'))")
    print("\nSQL:")
    print("UPDATE users SET hashed_password = 'NOVO_HASH_AQUI' WHERE username = 'admin';")
