"""Application configuration utilities and constants."""
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações JWT
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY não definida! "
        "Crie um arquivo .env com SECRET_KEY=sua-chave-secreta"
    )

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)

# Configurações de ambiente
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
IS_PRODUCTION = ENVIRONMENT == "production"

# CORS Origins - Configuração segura
if IS_PRODUCTION:
    # Em produção, ALLOWED_ORIGINS é obrigatório
    allowed_origins_str = os.getenv("ALLOWED_ORIGINS")
    if not allowed_origins_str:
        raise ValueError(
            "ALLOWED_ORIGINS não definida em produção! "
            "Defina ALLOWED_ORIGINS no .env com os domínios permitidos"
        )
    ALLOWED_ORIGINS = [origin.strip() for origin in allowed_origins_str.split(",")]
else:
    # Em desenvolvimento, usa localhost como fallback
    ALLOWED_ORIGINS = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:8000"
    ).split(",")
