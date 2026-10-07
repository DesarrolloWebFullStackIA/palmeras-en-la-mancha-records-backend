from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.album import Album
from app.models.album_format import AlbumFormat
from app.models.branch import Branch
from app.models.format import Format


def test_create_record_label_success(client: TestClient) -> None:
    """Test creating a record label with full information returns 201 Created.

    Assigned developer: Dev5 (TASK-10)
    """
    payload = {
        "name": "4AD",
        "country": "United Kingdom",
        "website": "https://4ad.com",
    }
    response = client.post("/api/v1/record-labels/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "4AD"
    assert data["country"] == "United Kingdom"
    assert data["website"] == "https://4ad.com"


def test_create_record_label_optional_website(client: TestClient) -> None:
    """Test creating a record label with optional website field omitted.

    Assigned developer: Dev5 (TASK-10)
    """
    payload = {
        "name": "Warp Records",
        "country": "United Kingdom",
    }
    response = client.post("/api/v1/record-labels/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Warp Records"
    assert data["website"] is None


def test_create_record_label_validation_error(client: TestClient) -> None:
    """Test validation failure (422) when mandatory fields are missing or invalid.

    Assigned developer: Dev5 (TASK-10)
    """
    # Missing 'country' and empty 'name'
    payload = {
        "name": "",
    }
    response = client.post("/api/v1/record-labels/", json=payload)

    assert response.status_code == 422


def test_get_all_record_labels(client: TestClient) -> None:
    """Test retrieving all record labels returns 200 OK with a list.

    Assigned developer: Dev5 (TASK-10)
    """
    client.post("/api/v1/record-labels/", json={"name": "Sub Pop", "country": "USA"})
    client.post("/api/v1/record-labels/", json={"name": "Matador", "country": "USA"})

    response = client.get("/api/v1/record-labels/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_record_label_by_id_success(client: TestClient) -> None:
    """Test retrieving an existing record label by ID returns 200 OK.

    Assigned developer: Dev5 (TASK-10)
    """
    create_res = client.post(
        "/api/v1/record-labels/",
        json={"name": "Rough Trade", "country": "United Kingdom", "website": "https://roughtrade.com"},
    )
    label_id = create_res.json()["id"]

    response = client.get(f"/api/v1/record-labels/{label_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == label_id
    assert data["name"] == "Rough Trade"


def test_get_record_label_not_found(client: TestClient) -> None:
    """Test retrieving a non-existent record label returns 404 Not Found.

    Assigned developer: Dev5 (TASK-10)
    """
    response = client.get("/api/v1/record-labels/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Record label not found"


def test_update_record_label_success(client: TestClient) -> None:
    """Test updating existing record label fields returns 200 OK.

    Assigned developer: Dev5 (TASK-10)
    """
    create_res = client.post(
        "/api/v1/record-labels/",
        json={"name": "Domino", "country": "UK"},
    )
    label_id = create_res.json()["id"]

    update_payload = {
        "name": "Domino Recording Company",
        "website": "https://dominomusic.com",
    }
    response = client.put(f"/api/v1/record-labels/{label_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == label_id
    assert data["name"] == "Domino Recording Company"
    assert data["country"] == "UK"
    assert data["website"] == "https://dominomusic.com"


def test_update_record_label_not_found(client: TestClient) -> None:
    """Test updating a non-existent record label returns 404 Not Found.

    Assigned developer: Dev5 (TASK-10)
    """
    response = client.put(
        "/api/v1/record-labels/99999",
        json={"name": "Nonexistent Label"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Record label not found"


def test_delete_record_label_success(client: TestClient) -> None:
    """Test deleting a record label returns 200 OK and removes it from the database.

    Assigned developer: Dev5 (TASK-10)
    """
    create_res = client.post(
        "/api/v1/record-labels/",
        json={"name": "Temporary Label", "country": "Spain"},
    )
    label_id = create_res.json()["id"]

    delete_res = client.delete(f"/api/v1/record-labels/{label_id}")

    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Record label deleted successfully"

    # Verify label no longer exists
    get_res = client.get(f"/api/v1/record-labels/{label_id}")
    assert get_res.status_code == 404


def test_delete_record_label_not_found(client: TestClient) -> None:
    """Test deleting a non-existent record label returns 404 Not Found.

    Assigned developer: Dev5 (TASK-10)
    """
    response = client.delete("/api/v1/record-labels/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Record label not found"


def test_include_albums_and_branch_filter(client: TestClient, db_session: Session) -> None:
    """Test retrieving record labels with nested albums and filtering by branch ID."""
    label_response = client.post(
        "/api/v1/record-labels/",
        json={
            "name": "Blue Note",
            "country": "United States",
            "website": "https://www.bluenote.com",
        },
    )
    label = label_response.json()

    stock_branch = Branch(
        name="Palmeras Madrid",
        address="Calle Mayor 1",
        phone="910000001",
    )
    other_branch = Branch(
        name="Palmeras Sevilla",
        address="Calle Sierpes 2",
        phone="910000002",
    )
    vinyl = Format(name="Vinyl")
    db_session.add_all([stock_branch, other_branch, vinyl])
    db_session.flush()

    album = Album(
        title="Kind of Blue",
        artist="Miles Davis",
        release_year=1959,
        label_id=label["id"],
    )
    db_session.add(album)
    db_session.flush()

    db_session.add(
        AlbumFormat(
            album_id=album.id,
            format_id=vinyl.id,
            branch_id=stock_branch.id,
            price=25.5,
            stock=5,
        )
    )
    db_session.commit()

    plain = client.get("/api/v1/record-labels/").json()
    assert plain[0]["albums"] == []

    nested = client.get("/api/v1/record-labels/?include_albums=true").json()
    assert [a["title"] for a in nested[0]["albums"]] == ["Kind of Blue"]

    nested_by_id = client.get(
        f"/api/v1/record-labels/{label['id']}?include_albums=true"
    ).json()
    assert [a["title"] for a in nested_by_id["albums"]] == ["Kind of Blue"]

    matching = client.get(f"/api/v1/record-labels/?branch_id={stock_branch.id}").json()
    assert [lbl["id"] for lbl in matching] == [label["id"]]

    without_stock = client.get(
        f"/api/v1/record-labels/?branch_id={other_branch.id}"
    ).json()
    assert without_stock == []
