from fastapi.testclient import TestClient

def test_register_user(test_client: TestClient):
    """
    Testa o registro de um novo usuário.
    """
    response = test_client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data


def test_login_for_access_token(test_client: TestClient):
    """
    Testa o login de um usuário e a obtenção de um token de acesso.
    """
    # Primeiro, registra um usuário para poder fazer login
    test_client.post(
        "/api/v1/auth/register",
        json={"username": "loginuser", "password": "loginpassword"},
    )
    
    # Agora, tenta fazer o login
    response = test_client.post(
        "/api/v1/auth/token",
        data={"username": "loginuser", "password": "loginpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
