import pytest
from fastapi.testclient import TestClient


def test_create_format_success(client: TestClient) -> None:
    """Test creating a physical format returns 201 Created.

    Assigned developer: Dev5 (TASK-10)
    """
    payload = {
        "name": "12\" Vinyl",
        "description": "Standard 12 inch vinyl record 33 RPM",
    }
    response = client.post("/api/v1/formats/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "12\" Vinyl"
    assert data["description"] == "Standard 12 inch vinyl record 33 RPM"


def test_create_format_optional_description(client: TestClient) -> None:
    """Test creating a format with optional description omitted.

    Assigned developer: Dev5 (TASK-10)
    """
    payload = {
        "name": "Compact Disc (CD)",
    }
    response = client.post("/api/v1/formats/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Compact Disc (CD)"
    assert data["description"] is None


def test_create_format_duplicate_name_error(client: TestClient) -> None:
    """Test that creating a format with duplicate name triggers 400 Bad Request.

    Assigned developer: Dev5 (TASK-10)
    """
    payload = {
        "name": "Cassette Tape",
        "description": "Magnetic audio cassette",
    }
    first_res = client.post("/api/v1/formats/", json=payload)
    assert first_res.status_code == 201

    duplicate_res = client.post(
        "/api/v1/formats/",
        json={"name": "Cassette Tape", "description": "Duplicate description"},
    )
    assert duplicate_res.status_code == 400
    assert "detail" in duplicate_res.json()


def test_create_format_validation_error(client: TestClient) -> None:
    """Test validation failure (422) when name is missing or invalid.

    Assigned developer: Dev5 (TASK-10)
    """
    response = client.post("/api/v1/formats/", json={"description": "Missing name"})

    assert response.status_code == 422


def test_get_all_formats(client: TestClient) -> None:
    """Test retrieving all formats returns 200 OK list.

    Assigned developer: Dev5 (TASK-10)
    """
    client.post("/api/v1/formats/", json={"name": "7\" Vinyl"})
    client.post("/api/v1/formats/", json={"name": "10\" Vinyl"})

    response = client.get("/api/v1/formats/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_format_by_id_success(client: TestClient) -> None:
    """Test retrieving a format by ID returns 200 OK.

    Assigned developer: Dev5 (TASK-10)
    """
    create_res = client.post(
        "/api/v1/formats/",
        json={"name": "MiniDisc", "description": "Optical magneto-disc"},
    )
    format_id = create_res.json()["id"]

    response = client.get(f"/api/v1/formats/{format_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == format_id
    assert data["name"] == "MiniDisc"


def test_get_format_not_found(client: TestClient) -> None:
    """Test retrieving a non-existent format returns 404 Not Found.

    Assigned developer: Dev5 (TASK-10)
    """
    response = client.get("/api/v1/formats/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Format not found"


def test_update_format_success(client: TestClient) -> None:
    """Test updating existing format fields returns 200 OK.

    Assigned developer: Dev5 (TASK-10)
    """
    create_res = client.post(
        "/api/v1/formats/",
        json={"name": "Reel to Reel", "description": "Original tape"},
    )
    format_id = create_res.json()["id"]

    update_payload = {
        "description": "1/4 inch master tape reel",
    }
    response = client.put(f"/api/v1/formats/{format_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == format_id
    assert data["name"] == "Reel to Reel"
    assert data["description"] == "1/4 inch master tape reel"


def test_update_format_not_found(client: TestClient) -> None:
    """Test updating a non-existent format returns 404 Not Found.

    Assigned developer: Dev5 (TASK-10)
    """
    response = client.put(
        "/api/v1/formats/99999",
        json={"name": "Nonexistent Format"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Format not found"


def test_update_format_duplicate_name_error(client: TestClient) -> None:
    """Test updating a format to an already existing name triggers 400 Bad Request.

    Assigned developer: Dev5 (TASK-10)
    """
    f1 = client.post("/api/v1/formats/", json={"name": "Format Alpha"}).json()["id"]
    f2 = client.post("/api/v1/formats/", json={"name": "Format Beta"}).json()["id"]

    response = client.put(f"/api/v1/formats/{f2}", json={"name": "Format Alpha"})

    assert response.status_code == 400
    assert "detail" in response.json()


def test_delete_format_success(client: TestClient) -> None:
    """Test deleting a format returns 204 No Content.

    Assigned developer: Dev5 (TASK-10)
    """
    create_res = client.post(
        "/api/v1/formats/",
        json={"name": "Obsolete Format"},
    )
    format_id = create_res.json()["id"]

    delete_res = client.delete(f"/api/v1/formats/{format_id}")

    assert delete_res.status_code == 204
    assert delete_res.content == b""

    # Verify format no longer exists
    get_res = client.get(f"/api/v1/formats/{format_id}")
    assert get_res.status_code == 404


def test_delete_format_not_found(client: TestClient) -> None:
    """Test deleting a non-existent format returns 404 Not Found.

    Assigned developer: Dev5 (TASK-10)
    """
    response = client.delete("/api/v1/formats/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Format not found"
