#!/usr/bin/env python3
"""Script para gerar SQL de criação de usuário de teste"""
import bcrypt

# Dados do novo usuário
USERNAME = "teste"
PASSWORD = "teste123"
EMAIL = "teste@hotel.com"
ROLE = "ADMIN"

# Gerar hash da senha
hashed_password = bcrypt.hashpw(PASSWORD.encode('utf-8'), bcrypt.gensalt())
hashed_password_str = hashed_password.decode('utf-8')

print("="*60)
print("🔐 USUÁRIO DE TESTE LOCAL")
print("="*60)
print(f"Username: {USERNAME}")
print(f"Password: {PASSWORD}")
print(f"Email: {EMAIL}")
print(f"Role: {ROLE}")
print("="*60)
print("\n📋 Execute este SQL no MySQL:\n")
print("="*60)

# SQL para deletar usuário existente (se houver)
print(f"-- Deletar usuário teste se existir")
print(f"DELETE FROM users WHERE username = '{USERNAME}' OR email = '{EMAIL}';")
print()

# SQL para inserir novo usuário
print(f"-- Criar novo usuário de teste")
print(f"INSERT INTO users (username, email, hashed_password, role, is_active, is_2fa_enabled, failed_login_attempts, created_at, updated_at)")
print(f"VALUES ('{USERNAME}', '{EMAIL}', '{hashed_password_str}', '{ROLE}', 1, 0, 0, NOW(), NOW());")
print()

# SQL para verificar
print(f"-- Verificar usuário criado")
print(f"SELECT id, username, email, role, is_active FROM users WHERE username = '{USERNAME}';")

print("="*60)
print("\n✅ Copie e cole os comandos acima no seu terminal MySQL!")
print("="*60)
