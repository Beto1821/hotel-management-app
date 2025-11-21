#!/usr/bin/env python
"""Script para testar o endpoint de login."""
import requests

# URL base da API
BASE_URL = "http://localhost:8000"

def test_login(username: str, password: str):
    """Testa o login com as credenciais fornecidas."""
    print(f"\n🔐 Testando login com usuário: {username}")
    print(f"📍 URL: {BASE_URL}/api/v1/auth/token")
    
    # Dados do formulário OAuth2
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login bem-sucedido!")
            token_data = response.json()
            print(f"🎫 Token: {token_data.get('access_token')[:50]}...")
            print(f"📝 Token Type: {token_data.get('token_type')}")
            return True
        else:
            print(f"❌ Falha no login!")
            print(f"📝 Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao fazer requisição: {e}")
        return False


if __name__ == "__main__":
    # Testar com o usuário existente
    print("=" * 60)
    print("TESTE DE LOGIN - Hotel Management API")
    print("=" * 60)
    
    # Primeiro teste - usuário teste/teste123
    test_login("teste", "teste123")
    
    print("\n" + "=" * 60)
