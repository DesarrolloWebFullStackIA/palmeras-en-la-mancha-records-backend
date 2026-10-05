from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient) -> None:
    """Test API root status endpoint.

    Assigned developer: Dev5 (TASK-05 smoke test)
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "version" in data
    assert "docs_url" in data


def test_health_check_endpoint(client: TestClient) -> None:
    """Test health check diagnostic endpoint verifying database connectivity.

    Assigned developer: Dev5 (TASK-05 smoke test)
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert "environment" in data
