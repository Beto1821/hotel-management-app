import pytest
from fastapi.testclient import TestClient
from datetime import date, timedelta


@pytest.fixture(scope="module")
def auth_headers(test_client: TestClient):
    """
    Cria um token compartilhado para autenticação entre os testes
    do módulo.
    """
    # Registra um usuário de teste
    test_client.post(
        "/api/v1/auth/register",
        json={
            "username": "quartouser",
            "email": "quartouser@example.com",
            "password": "QuartoTest123!"
        },
    )

    # Faz login para obter o token
    response = test_client.post(
        "/api/v1/auth/token",
        data={"username": "quartouser", "password": "QuartoTest123!"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_quarto_unauthorized(test_client: TestClient):
    """Testa a falha ao criar quarto sem autenticação."""
    response = test_client.post(
        "/api/v1/quartos/",
        json={
            "numero": "101",
            "tipo": "Standard",
            "preco_diaria": 150.00,
            "capacidade": 2,
        },
    )
    assert response.status_code == 401


def test_create_and_get_quarto(test_client: TestClient, auth_headers: dict):
    """Testa a criação e a busca de um quarto."""
    # Criar quarto
    quarto_data = {
        "numero": "102",
        "tipo": "deluxe",
        "valor_diaria": 350.00,
        "capacidade": 4,
        "descricao": "Quarto de luxo com vista para o mar"
    }
    response_create = test_client.post(
        "/api/v1/quartos/",
        json=quarto_data,
        headers=auth_headers,
    )
    assert response_create.status_code == 201
    created_quarto = response_create.json()
    assert created_quarto["numero"] == quarto_data["numero"]
    assert created_quarto["tipo"] == quarto_data["tipo"]
    assert float(created_quarto["valor_diaria"]) == quarto_data["valor_diaria"]
    quarto_id = created_quarto["id"]

    # Buscar o quarto criado
    response_get = test_client.get(
        f"/api/v1/quartos/{quarto_id}",
        headers=auth_headers,
    )
    assert response_get.status_code == 200
    fetched_quarto = response_get.json()
    assert fetched_quarto["numero"] == quarto_data["numero"]
    assert fetched_quarto["tipo"] == quarto_data["tipo"]


def test_get_non_existent_quarto(test_client: TestClient, auth_headers: dict):
    """Testa a busca por um quarto que não existe."""
    response = test_client.get("/api/v1/quartos/9999", headers=auth_headers)
    assert response.status_code == 404


def test_list_quartos(test_client: TestClient, auth_headers: dict):
    """Testa a listagem de quartos."""
    # Adiciona um quarto para garantir que a lista não esteja vazia
    test_client.post(
        "/api/v1/quartos/",
        json={
            "numero": "103",
            "tipo": "standard",
            "valor_diaria": 150.00,
            "capacidade": 2,
        },
        headers=auth_headers,
    )

    response = test_client.get("/api/v1/quartos/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_list_quartos_disponiveis(test_client: TestClient, auth_headers: dict):
    """Testa a listagem de quartos disponíveis."""
    # Cria um quarto disponível
    test_client.post(
        "/api/v1/quartos/",
        json={
            "numero": "104",
            "tipo": "standard",
            "valor_diaria": 150.00,
            "capacidade": 2,
            "status": "livre"
        },
        headers=auth_headers,
    )

    response = test_client.get(
        "/api/v1/quartos/",
        headers=auth_headers
    )
    assert response.status_code == 200
    quartos = response.json()
    assert isinstance(quartos, list)
    # Verifica que existem quartos livres
    quartos_livres = [q for q in quartos if q["status"] == "livre"]
    assert len(quartos_livres) > 0


def test_update_quarto(test_client: TestClient, auth_headers: dict):
    """Testa a atualização de um quarto."""
    # Cria um quarto para atualizar
    quarto_data = {
        "numero": "105",
        "tipo": "standard",
        "valor_diaria": 150.00,
        "capacidade": 2,
    }
    response_create = test_client.post(
        "/api/v1/quartos/",
        json=quarto_data,
        headers=auth_headers,
    )
    quarto_id = response_create.json()["id"]

    # Atualiza o preço e o tipo
    update_data = {
        "tipo": "deluxe",
        "valor_diaria": 450.00
    }
    response_update = test_client.put(
        f"/api/v1/quartos/{quarto_id}",
        json=update_data,
        headers=auth_headers,
    )
    assert response_update.status_code == 200
    updated_quarto = response_update.json()
    assert updated_quarto["tipo"] == "deluxe"
    assert float(updated_quarto["valor_diaria"]) == 450.00


def test_update_disponibilidade_quarto(test_client: TestClient, auth_headers: dict):
    """Testa a atualização de status de um quarto."""
    # Cria um quarto
    quarto_data = {
        "numero": "106",
        "tipo": "standard",
        "valor_diaria": 150.00,
        "capacidade": 2,
        "status": "livre"
    }
    response_create = test_client.post(
        "/api/v1/quartos/",
        json=quarto_data,
        headers=auth_headers,
    )
    quarto_id = response_create.json()["id"]

    # Marca como em manutenção
    response_update = test_client.put(
        f"/api/v1/quartos/{quarto_id}",
        json={"status": "manutencao"},
        headers=auth_headers,
    )
    assert response_update.status_code == 200
    assert response_update.json()["status"] == "manutencao"

    # Marca como livre novamente
    response_update2 = test_client.put(
        f"/api/v1/quartos/{quarto_id}",
        json={"status": "livre"},
        headers=auth_headers,
    )
    assert response_update2.status_code == 200
    assert response_update2.json()["status"] == "livre"


def test_delete_quarto(test_client: TestClient, auth_headers: dict):
    """Testa a exclusão de um quarto."""
    # Cria um quarto para deletar
    quarto_data = {
        "numero": "107",
        "tipo": "standard",
        "valor_diaria": 150.00,
        "capacidade": 2,
    }
    response_create = test_client.post(
        "/api/v1/quartos/",
        json=quarto_data,
        headers=auth_headers,
    )
    quarto_id = response_create.json()["id"]

    # Deleta o quarto
    response_delete = test_client.delete(
        f"/api/v1/quartos/{quarto_id}",
        headers=auth_headers,
    )
    assert response_delete.status_code == 204

    # Verifica se o quarto foi realmente deletado
    response_get = test_client.get(
        f"/api/v1/quartos/{quarto_id}",
        headers=auth_headers,
    )
    assert response_get.status_code == 404


def test_create_quarto_duplicate_numero(test_client: TestClient, auth_headers: dict):
    """Testa a criação de quarto com número duplicado."""
    quarto_data = {
        "numero": "108",
        "tipo": "standard",
        "valor_diaria": 150.00,
        "capacidade": 2,
    }
    
    # Cria o primeiro quarto
    response1 = test_client.post(
        "/api/v1/quartos/",
        json=quarto_data,
        headers=auth_headers,
    )
    assert response1.status_code == 201

    # Tenta criar outro quarto com o mesmo número
    response2 = test_client.post(
        "/api/v1/quartos/",
        json=quarto_data,
        headers=auth_headers,
    )
    assert response2.status_code == 409  # Conflict


def test_create_quarto_invalid_data(test_client: TestClient, auth_headers: dict):
    """Testa a criação de quarto com dados inválidos."""
    # Tipo inválido (não está no enum)
    quarto_data = {
        "numero": "109",
        "tipo": "presidencial",  # Não existe no enum
        "valor_diaria": 50.00,
        "capacidade": 2,
    }
    response = test_client.post(
        "/api/v1/quartos/",
        json=quarto_data,
        headers=auth_headers,
    )
    assert response.status_code == 422  # Unprocessable Entity

    # Sem número (campo obrigatório)
    quarto_data2 = {
        "tipo": "standard",
        "valor_diaria": 150.00,
        "capacidade": 2,
    }
    response2 = test_client.post(
        "/api/v1/quartos/",
        json=quarto_data2,
        headers=auth_headers,
    )
    assert response2.status_code == 422
