"""
Utilitários para extrair informações de requisições HTTP
"""
from typing import Optional
from fastapi import Request


def get_client_ip(request: Request) -> Optional[str]:
    """
    Extrai o endereço IP do cliente da requisição.
    
    Verifica headers de proxy (X-Forwarded-For, X-Real-IP) primeiro,
    depois usa o IP direto da conexão.
    
    Args:
        request: Objeto Request do FastAPI
        
    Returns:
        str: Endereço IP do cliente, ou None se não puder determinar
    """
    # Tenta obter IP de headers de proxy
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # X-Forwarded-For pode conter múltiplos IPs, pega o primeiro
        return forwarded.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()
    
    # Fallback para o IP direto da conexão
    if request.client:
        return request.client.host
    
    return None


def get_user_agent(request: Request) -> Optional[str]:
    """
    Extrai o User-Agent do cliente da requisição.
    
    Args:
        request: Objeto Request do FastAPI
        
    Returns:
        str: String do User-Agent, ou None se não disponível
    """
    return request.headers.get("User-Agent")


def get_client_info(request: Request) -> dict:
    """
    Extrai informações completas do cliente da requisição.
    
    Args:
        request: Objeto Request do FastAPI
        
    Returns:
        dict: Dicionário com ip_address e user_agent
    """
    return {
        "ip_address": get_client_ip(request),
        "user_agent": get_user_agent(request)
    }
