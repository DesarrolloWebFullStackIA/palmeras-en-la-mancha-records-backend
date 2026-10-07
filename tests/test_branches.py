import pytest
from fastapi.testclient import TestClient


def test_create_branch_success(client: TestClient) -> None:
    """Test creating a physical store branch returns 201 Created.

    Assigned developer: Dev5 (TASK-10)
    """
    payload = {
        "name": "Palmeras Madrid Central",
        "address": "Calle del Pez 21, Malasaña",
        "phone": "+34912345678",
    }
    response = client.post("/api/v1/branches/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Palmeras Madrid Central"
    assert data["address"] == "Calle del Pez 21, Malasaña"
    assert data["phone"] == "+34912345678"


def test_create_branch_optional_address(client: TestClient) -> None:
    """Test creating a branch with optional address omitted.

    Assigned developer: Dev5 (TASK-10)
    """
    payload = {
        "name": "Palmeras Barcelona Pop-Up",
        "phone": "+34934567890",
    }
    response = client.post("/api/v1/branches/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Palmeras Barcelona Pop-Up"
    assert data["address"] is None
    assert data["phone"] == "+34934567890"


def test_create_branch_validation_error(client: TestClient) -> None:
    """Test validation failure (422) when mandatory fields (e.g. phone) are missing.

    Assigned developer: Dev5 (TASK-10)
    """
    payload = {
        "name": "Incomplete Store",
    }
    response = client.post("/api/v1/branches/", json=payload)

    assert response.status_code == 422


def test_get_all_branches(client: TestClient) -> None:
    """Test retrieving all branches returns 200 OK list.

    Assigned developer: Dev5 (TASK-10)
    """
    client.post("/api/v1/branches/", json={"name": "Sucursal Toledo", "phone": "+34925000000"})
    client.post("/api/v1/branches/", json={"name": "Sucursal Albacete", "phone": "+34967000000"})

    response = client.get("/api/v1/branches/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_branch_by_id_success(client: TestClient) -> None:
    """Test retrieving a branch by ID returns 200 OK.

    Assigned developer: Dev5 (TASK-10)
    """
    create_res = client.post(
        "/api/v1/branches/",
        json={"name": "Sucursal Cuenca", "address": "Plaza Mayor 5", "phone": "+34969000000"},
    )
    branch_id = create_res.json()["id"]

    response = client.get(f"/api/v1/branches/{branch_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == branch_id
    assert data["name"] == "Sucursal Cuenca"


def test_get_branch_not_found(client: TestClient) -> None:
    """Test retrieving a non-existent branch returns 404 Not Found.

    Assigned developer: Dev5 (TASK-10)
    """
    response = client.get("/api/v1/branches/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Branch not found"


def test_update_branch_success(client: TestClient) -> None:
    """Test updating existing branch details returns 200 OK.

    Assigned developer: Dev5 (TASK-10)
    """
    create_res = client.post(
        "/api/v1/branches/",
        json={"name": "Sucursal Ciudad Real", "phone": "+34926000000"},
    )
    branch_id = create_res.json()["id"]

    update_payload = {
        "address": "Calle Mayor 14, Ciudad Real",
        "phone": "+34926111222",
    }
    response = client.put(f"/api/v1/branches/{branch_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == branch_id
    assert data["name"] == "Sucursal Ciudad Real"
    assert data["address"] == "Calle Mayor 14, Ciudad Real"
    assert data["phone"] == "+34926111222"


def test_update_branch_not_found(client: TestClient) -> None:
    """Test updating a non-existent branch returns 404 Not Found.

    Assigned developer: Dev5 (TASK-10)
    """
    response = client.put(
        "/api/v1/branches/99999",
        json={"name": "Ghost Branch"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Branch not found"


def test_delete_branch_success(client: TestClient) -> None:
    """Test deleting a branch returns 204 No Content.

    Assigned developer: Dev5 (TASK-10)
    """
    create_res = client.post(
        "/api/v1/branches/",
        json={"name": "Temporary Store", "phone": "+34900000000"},
    )
    branch_id = create_res.json()["id"]

    delete_res = client.delete(f"/api/v1/branches/{branch_id}")

    assert delete_res.status_code == 204
    assert delete_res.content == b""

    # Verify branch no longer exists
    get_res = client.get(f"/api/v1/branches/{branch_id}")
    assert get_res.status_code == 404


def test_delete_branch_not_found(client: TestClient) -> None:
    """Test deleting a non-existent branch returns 404 Not Found.

    Assigned developer: Dev5 (TASK-10)
    """
    response = client.delete("/api/v1/branches/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Branch not found"
