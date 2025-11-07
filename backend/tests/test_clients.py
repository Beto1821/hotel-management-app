import pytest
from fastapi.testclient import TestClient

# Fixture para obter cabeçalhos de autenticação.
# 'scope="module"' faz com que seja executado apenas uma vez para todos os testes neste arquivo.
@pytest.fixture(scope="module")
def auth_headers(test_client: TestClient):
    # Registra um usuário de teste
    test_client.post(
        "/api/v1/auth/register",
        json={"username": "clienttestuser", "password": "testpassword"},
    )
    
    # Faz login para obter o token
    response = test_client.post(
        "/api/v1/auth/token",
        data={"username": "clienttestuser", "password": "testpassword"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_client_unauthorized(test_client: TestClient):
    """Testa a falha ao criar cliente sem autenticação."""
    response = test_client.post(
        "/api/v1/clients/",
        json={"name": "Test Client", "email": "test@example.com", "phone": "1234567890", "document": "123.456.789-00"},
    )
    assert response.status_code == 401


def test_create_and_get_client(test_client: TestClient, auth_headers: dict):
    """Testa a criação e a busca de um cliente."""
    # Criar cliente
    client_data = {"name": "New Client", "email": "new@example.com", "phone": "9876543210", "document": "987.654.321-00"}
    response_create = test_client.post("/api/v1/clients/", json=client_data, headers=auth_headers)
    assert response_create.status_code == 201
    created_client = response_create.json()
    assert created_client["name"] == client_data["name"]
    client_id = created_client["id"]

    # Buscar o cliente criado
    response_get = test_client.get(f"/api/v1/clients/{client_id}", headers=auth_headers)
    assert response_get.status_code == 200
    fetched_client = response_get.json()
    assert fetched_client["name"] == client_data["name"]


def test_get_non_existent_client(test_client: TestClient, auth_headers: dict):
    """Testa a busca por um cliente que não existe."""
    response = test_client.get("/api/v1/clients/9999", headers=auth_headers)
    assert response.status_code == 404


def test_list_clients(test_client: TestClient, auth_headers: dict):
    """Testa a listagem de clientes."""
    # Adiciona um cliente para garantir que a lista não esteja vazia
    test_client.post("/api/v1/clients/", json={"name": "List Test Client", "email": "list@example.com", "phone": "111222333", "document": "111.222.333-44"}, headers=auth_headers)
    
    response = test_client.get("/api/v1/clients/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_update_client(test_client: TestClient, auth_headers: dict):
    """Testa a atualização de um cliente."""
    # Cria um cliente para atualizar
    client_data = {"name": "Update Me", "email": "update@example.com", "phone": "555555555", "document": "555.555.555-55"}
    response_create = test_client.post("/api/v1/clients/", json=client_data, headers=auth_headers)
    client_id = response_create.json()["id"]

    # Atualiza o nome
    update_data = {"name": "Updated Name"}
    response_update = test_client.put(f"/api/v1/clients/{client_id}", json=update_data, headers=auth_headers)
    assert response_update.status_code == 200
    assert response_update.json()["name"] == "Updated Name"


def test_delete_client(test_client: TestClient, auth_headers: dict):
    """Testa a exclusão de um cliente."""
    # Cria um cliente para deletar
    client_data = {"name": "Delete Me", "email": "delete@example.com", "phone": "444444444", "document": "444.444.444-44"}
    response_create = test_client.post("/api/v1/clients/", json=client_data, headers=auth_headers)
    client_id = response_create.json()["id"]

    # Deleta o cliente
    response_delete = test_client.delete(f"/api/v1/clients/{client_id}", headers=auth_headers)
    assert response_delete.status_code == 204 # 204 No Content é o esperado para delete

    # Verifica se o cliente foi realmente deletado
    response_get = test_client.get(f"/api/v1/clients/{client_id}", headers=auth_headers)
    assert response_get.status_code == 404
