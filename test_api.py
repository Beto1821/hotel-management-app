#!/usr/bin/env python3
"""Quick health check script for the FastAPI backend."""

import json
from urllib import error, request


def _call_endpoint(url: str):
    """Perform a simple HTTP GET using only the standard library."""
    with request.urlopen(url) as response:
        status = response.status
        body = response.read().decode()
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = body
    return status, payload


def test_api():
    try:
        # Testar endpoint raiz
        print("🔍 Testando endpoint raiz...")
        status, payload = _call_endpoint("http://localhost:8000/")
        print(f"Status: {status}")
        print(f"Response: {payload}")
        print()

        # Testar health check
        print("🔍 Testando health check...")
        status, payload = _call_endpoint("http://localhost:8000/health")
        print(f"Status: {status}")
        print(f"Response: {payload}")
        print()

        # Testar documentação da API
        print("🔍 Testando documentação...")
        status, _ = _call_endpoint("http://localhost:8000/docs")
        print(f"Status da documentação: {status}")

        print("✅ Backend API está funcionando!")

    except error.URLError:
        print("❌ Erro: Não foi possível conectar ao servidor backend")
        print("   Verifique se o servidor roda em http://localhost:8000")
    except Exception as exc:  # pragma: no cover - saída de debug manual
        print(f"❌ Erro inesperado: {exc}")


if __name__ == "__main__":
    test_api()
