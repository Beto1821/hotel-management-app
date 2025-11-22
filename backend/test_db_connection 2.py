#!/usr/bin/env python
"""Script para testar a conexão com o banco de dados."""
import sys
from sqlalchemy import create_engine, text

# Importar as configurações do database.py
from core.database import DATABASE_URL, engine

def test_connection():
    """Testa a conexão com o banco de dados."""
    print("🔍 Testando conexão com o banco de dados...")
    print(f"📍 URL: {DATABASE_URL.split('@')[-1]}")  # Não mostra senha
    
    try:
        # Testar conexão
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexão estabelecida com sucesso!")
            
            # Verificar banco de dados
            result = conn.execute(text("SELECT DATABASE()"))
            db_name = result.scalar()
            print(f"📊 Banco de dados conectado: {db_name}")
            
            # Listar tabelas
            result = conn.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            if tables:
                print(f"📋 Tabelas existentes: {len(tables)}")
                for table in tables:
                    print(f"   - {table[0]}")
            else:
                print("📋 Nenhuma tabela criada ainda (normal na primeira execução)")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
