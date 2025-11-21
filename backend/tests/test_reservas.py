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
            "username": "reservauser",
            "email": "reservauser@example.com",
            "password": "ReservaTest123!"
        },
    )

    # Faz login para obter o token
    response = test_client.post(
        "/api/v1/auth/token",
        data={"username": "reservauser", "password": "ReservaTest123!"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def test_client_data(test_client: TestClient, auth_headers: dict):
    """Cria um cliente de teste para usar nas reservas."""
    import time
    client_data = {
        "name": "Cliente Reserva",
        "email": f"reserva{int(time.time() * 1000)}@example.com",
        "phone": "123456789",
        "document": f"{int(time.time() * 1000) % 100000000000}",
    }
    response = test_client.post(
        "/api/v1/clients/",
        json=client_data,
        headers=auth_headers,
    )
    return response.json()


@pytest.fixture(scope="function")
def test_quarto_data(test_client: TestClient, auth_headers: dict):
    """Cria um quarto de teste para usar nas reservas."""
    import time
    quarto_data = {
        "numero": f"Q{int(time.time() * 1000) % 100000}",
        "tipo": "standard",
        "valor_diaria": 200.00,
        "capacidade": 2,
        "status": "livre"
    }
    response = test_client.post(
        "/api/v1/quartos/",
        json=quarto_data,
        headers=auth_headers,
    )
    return response.json()


def test_create_reserva_unauthorized(test_client: TestClient):
    """Testa a falha ao criar reserva sem autenticação."""
    hoje = date.today()
    amanha = hoje + timedelta(days=1)

    response = test_client.post(
        "/api/v1/reservas/",
        json={
            "client_id": 1,
            "quarto_id": 1,
            "data_checkin": str(hoje),
            "data_checkout": str(amanha),
        },
    )
    assert response.status_code == 401


def test_create_and_get_reserva(
    test_client: TestClient,
    auth_headers: dict,
    test_client_data: dict,
    test_quarto_data: dict
):
    """Testa a criação e a busca de uma reserva."""
    hoje = date.today()
    checkout = hoje + timedelta(days=3)

    # Criar reserva
    reserva_data = {
        "client_id": test_client_data["id"],
        "quarto_id": test_quarto_data["id"],
        "data_checkin": str(hoje),
        "data_checkout": str(checkout)
    }
    response_create = test_client.post(
        "/api/v1/reservas/",
        json=reserva_data,
        headers=auth_headers,
    )
    assert response_create.status_code == 201
    created_reserva = response_create.json()
    assert created_reserva["client_id"] == reserva_data["client_id"]
    assert created_reserva["quarto_id"] == reserva_data["quarto_id"]
    reserva_id = created_reserva["id"]

    # Buscar a reserva criada
    response_get = test_client.get(
        f"/api/v1/reservas/{reserva_id}",
        headers=auth_headers,
    )
    assert response_get.status_code == 200
    fetched_reserva = response_get.json()
    assert fetched_reserva["id"] == reserva_id
    assert fetched_reserva["status"] == "pendente"


def test_get_non_existent_reserva(test_client: TestClient, auth_headers: dict):
    """Testa a busca por uma reserva que não existe."""
    response = test_client.get("/api/v1/reservas/9999", headers=auth_headers)
    assert response.status_code == 404


def test_list_reservas(
    test_client: TestClient,
    auth_headers: dict,
    test_client_data: dict,
    test_quarto_data: dict
):
    """Testa a listagem de reservas."""
    hoje = date.today()
    checkout = hoje + timedelta(days=2)

    # Adiciona uma reserva para garantir que a lista não esteja vazia
    test_client.post(
        "/api/v1/reservas/",
        json={
            "client_id": test_client_data["id"],
            "quarto_id": test_quarto_data["id"],
            "data_checkin": str(hoje),
            "data_checkout": str(checkout),
        },
        headers=auth_headers,
    )

    response = test_client.get("/api/v1/reservas/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_update_reserva_status(
    test_client: TestClient,
    auth_headers: dict,
    test_client_data: dict,
    test_quarto_data: dict
):
    """Testa a atualização do status de uma reserva."""
    hoje = date.today()
    checkout = hoje + timedelta(days=2)

    # Cria uma reserva
    reserva_data = {
        "client_id": test_client_data["id"],
        "quarto_id": test_quarto_data["id"],
        "data_checkin": str(hoje),
        "data_checkout": str(checkout),
    }
    response_create = test_client.post(
        "/api/v1/reservas/",
        json=reserva_data,
        headers=auth_headers,
    )
    assert response_create.status_code == 201, (
        f"Expected 201, got {response_create.status_code}: "
        f"{response_create.text}"
    )
    reserva_id = response_create.json()["id"]

    # Atualiza o status para confirmada
    response_update = test_client.put(
        f"/api/v1/reservas/{reserva_id}",
        json={"status": "confirmada"},
        headers=auth_headers,
    )
    assert response_update.status_code == 200
    assert response_update.json()["status"] == "confirmada"

    # Atualiza para checkin
    response_checkin = test_client.put(
        f"/api/v1/reservas/{reserva_id}",
        json={"status": "checkin"},
        headers=auth_headers,
    )
    assert response_checkin.status_code == 200
    assert response_checkin.json()["status"] == "checkin"

    # Atualiza para checkout
    response_checkout = test_client.put(
        f"/api/v1/reservas/{reserva_id}",
        json={"status": "checkout"},
        headers=auth_headers,
    )
    assert response_checkout.status_code == 200
    assert response_checkout.json()["status"] == "checkout"


def test_update_reserva(
    test_client: TestClient,
    auth_headers: dict,
    test_client_data: dict,
    test_quarto_data: dict
):
    """Testa a atualização de uma reserva."""
    hoje = date.today()
    checkout = hoje + timedelta(days=2)

    # Cria uma reserva
    reserva_data = {
        "client_id": test_client_data["id"],
        "quarto_id": test_quarto_data["id"],
        "data_checkin": str(hoje),
        "data_checkout": str(checkout),
    }
    response_create = test_client.post(
        "/api/v1/reservas/",
        json=reserva_data,
        headers=auth_headers,
    )
    assert response_create.status_code == 201, (
        f"Expected 201, got {response_create.status_code}: "
        f"{response_create.text}"
    )
    reserva_id = response_create.json()["id"]

    # Atualiza a data de checkout
    novo_checkout = hoje + timedelta(days=5)
    update_data = {
        "data_checkout": str(novo_checkout)
    }
    response_update = test_client.put(
        f"/api/v1/reservas/{reserva_id}",
        json=update_data,
        headers=auth_headers,
    )
    assert response_update.status_code == 200
    updated_reserva = response_update.json()
    assert updated_reserva["data_checkout"] == str(novo_checkout)


def test_cancel_reserva(
    test_client: TestClient,
    auth_headers: dict,
    test_client_data: dict,
    test_quarto_data: dict
):
    """Testa o cancelamento de uma reserva."""
    hoje = date.today()
    checkout = hoje + timedelta(days=2)

    # Cria uma reserva
    reserva_data = {
        "client_id": test_client_data["id"],
        "quarto_id": test_quarto_data["id"],
        "data_checkin": str(hoje),
        "data_checkout": str(checkout),
    }
    response_create = test_client.post(
        "/api/v1/reservas/",
        json=reserva_data,
        headers=auth_headers,
    )
    assert response_create.status_code == 201, (
        f"Expected 201, got {response_create.status_code}: "
        f"{response_create.text}"
    )
    reserva_id = response_create.json()["id"]

    # Cancela a reserva
    response_cancel = test_client.put(
        f"/api/v1/reservas/{reserva_id}",
        json={"status": "cancelada"},
        headers=auth_headers,
    )
    assert response_cancel.status_code == 200
    assert response_cancel.json()["status"] == "cancelada"


def test_delete_reserva(
    test_client: TestClient,
    auth_headers: dict,
    test_client_data: dict,
    test_quarto_data: dict
):
    """Testa a exclusão de uma reserva."""
    hoje = date.today()
    checkout = hoje + timedelta(days=2)

    # Cria uma reserva para deletar
    reserva_data = {
        "client_id": test_client_data["id"],
        "quarto_id": test_quarto_data["id"],
        "data_checkin": str(hoje),
        "data_checkout": str(checkout),
    }
    response_create = test_client.post(
        "/api/v1/reservas/",
        json=reserva_data,
        headers=auth_headers,
    )
    assert response_create.status_code == 201, (
        f"Expected 201, got {response_create.status_code}: "
        f"{response_create.text}"
    )
    reserva_id = response_create.json()["id"]

    # Deleta a reserva
    response_delete = test_client.delete(
        f"/api/v1/reservas/{reserva_id}",
        headers=auth_headers,
    )
    assert response_delete.status_code == 200
    deleted_reserva = response_delete.json()
    assert deleted_reserva["status"] == "cancelada"

    # Verifica que a reserva foi cancelada, não deletada
    response_get = test_client.get(
        f"/api/v1/reservas/{reserva_id}",
        headers=auth_headers,
    )
    assert response_get.status_code == 200
    assert response_get.json()["status"] == "cancelada"


def test_create_reserva_invalid_dates(
    test_client: TestClient,
    auth_headers: dict,
    test_client_data: dict,
    test_quarto_data: dict
):
    """Testa a criação de reserva com datas inválidas."""
    hoje = date.today()
    ontem = hoje - timedelta(days=1)

    # Checkout antes do checkin
    reserva_data = {
        "client_id": test_client_data["id"],
        "quarto_id": test_quarto_data["id"],
        "data_checkin": str(hoje),
        "data_checkout": str(ontem),
    }
    response = test_client.post(
        "/api/v1/reservas/",
        json=reserva_data,
        headers=auth_headers,
    )
    assert response.status_code == 400  # Bad Request


def test_create_reserva_past_date(
    test_client: TestClient,
    auth_headers: dict,
    test_client_data: dict,
    test_quarto_data: dict
):
    """Testa a criação de reserva com data no passado."""
    passado = date.today() - timedelta(days=10)
    checkout = passado + timedelta(days=2)

    reserva_data = {
        "client_id": test_client_data["id"],
        "quarto_id": test_quarto_data["id"],
        "data_checkin": str(passado),
        "data_checkout": str(checkout),
    }
    response = test_client.post(
        "/api/v1/reservas/",
        json=reserva_data,
        headers=auth_headers,
    )
    # Como não há validação de data passada, aceita
    assert response.status_code == 201


def test_list_reservas_by_cliente(
    test_client: TestClient,
    auth_headers: dict,
    test_client_data: dict,
    test_quarto_data: dict
):
    """Testa a listagem de reservas filtrando por cliente."""
    hoje = date.today()
    checkout = hoje + timedelta(days=2)

    # Cria uma reserva para o cliente
    reserva_data = {
        "client_id": test_client_data["id"],
        "quarto_id": test_quarto_data["id"],
        "data_checkin": str(hoje),
        "data_checkout": str(checkout),
    }
    test_client.post(
        "/api/v1/reservas/",
        json=reserva_data,
        headers=auth_headers,
    )

    # Lista todas as reservas e filtra manualmente
    response = test_client.get(
        "/api/v1/reservas/",
        headers=auth_headers,
    )
    assert response.status_code == 200
    reservas = response.json()
    assert isinstance(reservas, list)
    # Verifica que há pelo menos uma reserva do cliente
    client_id = test_client_data["id"]
    reservas_cliente = [r for r in reservas if r["client_id"] == client_id]
    assert len(reservas_cliente) > 0


def test_list_reservas_by_quarto(
    test_client: TestClient,
    auth_headers: dict,
    test_client_data: dict,
    test_quarto_data: dict
):
    """Testa a listagem de reservas filtrando por quarto."""
    hoje = date.today()
    checkout = hoje + timedelta(days=2)

    # Cria uma reserva para o quarto
    reserva_data = {
        "client_id": test_client_data["id"],
        "quarto_id": test_quarto_data["id"],
        "data_checkin": str(hoje),
        "data_checkout": str(checkout),
    }
    test_client.post(
        "/api/v1/reservas/",
        json=reserva_data,
        headers=auth_headers,
    )

    # Lista todas as reservas e filtra manualmente
    response = test_client.get(
        "/api/v1/reservas/",
        headers=auth_headers,
    )
    assert response.status_code == 200
    reservas = response.json()
    assert isinstance(reservas, list)
    # Verifica que há pelo menos uma reserva do quarto
    quarto_id = test_quarto_data["id"]
    reservas_quarto = [r for r in reservas if r["quarto_id"] == quarto_id]
    assert len(reservas_quarto) > 0
