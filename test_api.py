#!/usr/bin/env python3
import requests
import json

def test_api():
    try:
        # Testar endpoint raiz
        print("🔍 Testando endpoint raiz...")
        response = requests.get("http://localhost:8000/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        
        # Testar health check
        print("🔍 Testando health check...")
        response = requests.get("http://localhost:8000/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        
        # Testar documentação da API
        print("🔍 Testando documentação...")
        response = requests.get("http://localhost:8000/docs")
        print(f"Status da documentação: {response.status_code}")
        
        print("✅ Backend API está funcionando!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor backend")
        print("   Verifique se o servidor está rodando em http://localhost:8000")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    test_api()