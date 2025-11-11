#!/usr/bin/env python3
"""
Script para testar a conexão com o MySQL
"""
import os
from urllib.parse import unquote
from dotenv import load_dotenv
import pymysql

# Carregar variáveis do arquivo .env
load_dotenv()

def test_mysql_connection():
    """Testa a conexão com o MySQL usando as credenciais do .env"""
    
    database_url = os.getenv("DATABASE_URL")
    print(f"DATABASE_URL: {database_url}")
    
    if not database_url:
        print("❌ DATABASE_URL não encontrada no arquivo .env")
        return False
    
    # Parse da URL para extrair as credenciais
    if database_url.startswith("mysql+pymysql://"):
        # Formato: mysql+pymysql://user:password@host:port/dbname
        parts = database_url.replace("mysql+pymysql://", "").split("/")
        db_name = parts[1] if len(parts) > 1 else ""
        
        user_pass_host = parts[0].split("@")
        host_port = user_pass_host[1].split(":") if len(user_pass_host) > 1 else ["localhost", "3306"]
        host = host_port[0]
        port = int(host_port[1]) if len(host_port) > 1 else 3306
        
        user_pass = user_pass_host[0].split(":")
        user = user_pass[0]
        password = unquote(user_pass[1]) if len(user_pass) > 1 else ""  # Decodifica a senha
        
        print(f"Tentando conectar com:")
        print(f"  Host: {host}")
        print(f"  Port: {port}")
        print(f"  User: {user}")
        print(f"  Password: {'*' * len(password)}")
        print(f"  Database: {db_name}")
        
        try:
            # Testar conexão
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=db_name,
                charset='utf8mb4'
            )
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"✅ Conexão bem-sucedida! MySQL Version: {version[0]}")
                
                # Verificar se o banco existe
                cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
                db_exists = cursor.fetchone()
                if db_exists:
                    print(f"✅ Banco de dados '{db_name}' encontrado!")
                    
                    # Verificar tabelas
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    if tables:
                        print(f"✅ Tabelas encontradas: {[table[0] for table in tables]}")
                    else:
                        print("⚠️  Nenhuma tabela encontrada no banco")
                else:
                    print(f"❌ Banco de dados '{db_name}' não existe!")
                    
            connection.close()
            return True
            
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            return False
    else:
        print("❌ Formato de DATABASE_URL inválido")
        return False

if __name__ == "__main__":
    test_mysql_connection()