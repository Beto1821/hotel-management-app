import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Adiciona o diretório raiz do projeto ao path para encontrar o .env
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
load_dotenv(dotenv_path=project_root / ".env")


def check_database_connection():
    """
    Verifica a conexão com o banco de dados usando a DATABASE_URL do ambiente.
    """
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ Erro: A variável de ambiente DATABASE_URL não foi encontrada.")
        print("Certifique-se de que o arquivo .env existe na pasta 'backend/'.")
        return

    print(f"⏳ Tentando conectar ao banco de dados em: {db_url.split('@')[-1]}")

    try:
        engine = create_engine(db_url)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("✅ Sucesso! A conexão com o banco de dados foi estabelecida.")
    except OperationalError as e:
        print(f"❌ Falha na conexão: {e}")
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    check_database_connection()
