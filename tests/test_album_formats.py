import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.album import Album
from app.models.album_format import AlbumFormat
from app.models.branch import Branch
from app.models.format import Format
from app.models.record_label import RecordLabel


@pytest.fixture
def setup_parents(db_session: Session) -> dict:
    """Create parent entities required for album_format relations."""
    label = RecordLabel(name="Sub Pop", country="USA")
    db_session.add(label)
    db_session.commit()
    db_session.refresh(label)

    album = Album(
        title="Bleach",
        artist="Nirvana",
        release_year=1989,
        genre="Grunge",
        label_id=label.id,
    )
    fmt = Format(name="Vinyl LP 12\"", description="Standard 12 inch vinyl")
    branch = Branch(name="Madrid Central", address="Gran Via 12", phone="+34912345678")

    db_session.add_all([album, fmt, branch])
    db_session.commit()
    db_session.refresh(album)
    db_session.refresh(fmt)
    db_session.refresh(branch)

    return {
        "label": label,
        "album": album,
        "format": fmt,
        "branch": branch,
    }


def test_create_album_format_success(client: TestClient, setup_parents: dict) -> None:
    """Test creating an album format inventory link returns 201 Created.

    Assigned developer: Dev5 (TASK-20)
    """
    payload = {
        "album_id": setup_parents["album"].id,
        "format_id": setup_parents["format"].id,
        "branch_id": setup_parents["branch"].id,
        "price": 24.99,
        "stock": 15,
    }
    response = client.post("/api/v1/album-formats/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["album_id"] == setup_parents["album"].id
    assert data["format_id"] == setup_parents["format"].id
    assert data["branch_id"] == setup_parents["branch"].id
    assert data["price"] == 24.99
    assert data["stock"] == 15
    assert data["format"]["name"] == "Vinyl LP 12\""
    assert data["branch"]["name"] == "Madrid Central"


def test_get_all_album_formats(client: TestClient, setup_parents: dict) -> None:
    """Test retrieving all album format inventory records returns 200 OK list.

    Assigned developer: Dev5 (TASK-20)
    """
    payload = {
        "album_id": setup_parents["album"].id,
        "format_id": setup_parents["format"].id,
        "branch_id": setup_parents["branch"].id,
        "price": 19.99,
        "stock": 8,
    }
    client.post("/api/v1/album-formats/", json=payload)

    response = client.get("/api/v1/album-formats/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_album_format_by_id_success(client: TestClient, setup_parents: dict) -> None:
    """Test retrieving an album format edition by ID returns 200 OK.

    Assigned developer: Dev5 (TASK-20)
    """
    create_res = client.post(
        "/api/v1/album-formats/",
        json={
            "album_id": setup_parents["album"].id,
            "format_id": setup_parents["format"].id,
            "branch_id": setup_parents["branch"].id,
            "price": 22.50,
            "stock": 5,
        },
    )
    af_id = create_res.json()["id"]

    response = client.get(f"/api/v1/album-formats/{af_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == af_id
    assert data["price"] == 22.50
    assert data["stock"] == 5


def test_get_album_format_not_found(client: TestClient) -> None:
    """Test retrieving a non-existent album format returns 404 Not Found.

    Assigned developer: Dev5 (TASK-20)
    """
    response = client.get("/api/v1/album-formats/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Album format not found"


def test_update_album_format_price_and_stock(client: TestClient, setup_parents: dict) -> None:
    """Test updating price and stock for an existing edition returns 200 OK.

    Assigned developer: Dev5 (TASK-20)
    """
    create_res = client.post(
        "/api/v1/album-formats/",
        json={
            "album_id": setup_parents["album"].id,
            "format_id": setup_parents["format"].id,
            "branch_id": setup_parents["branch"].id,
            "price": 20.0,
            "stock": 10,
        },
    )
    af_id = create_res.json()["id"]

    update_payload = {
        "price": 28.50,
        "stock": 45,
    }
    response = client.put(f"/api/v1/album-formats/{af_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == af_id
    assert data["price"] == 28.50
    assert data["stock"] == 45


def test_update_album_format_not_found(client: TestClient) -> None:
    """Test updating a non-existent album format returns 404 Not Found.

    Assigned developer: Dev5 (TASK-20)
    """
    response = client.put(
        "/api/v1/album-formats/99999",
        json={"price": 15.0, "stock": 10},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Album format not found"


def test_delete_album_format_success(client: TestClient, setup_parents: dict) -> None:
    """Test deleting an album format edition returns 204 No Content.

    Assigned developer: Dev5 (TASK-20)
    """
    create_res = client.post(
        "/api/v1/album-formats/",
        json={
            "album_id": setup_parents["album"].id,
            "format_id": setup_parents["format"].id,
            "branch_id": setup_parents["branch"].id,
            "price": 18.0,
            "stock": 3,
        },
    )
    af_id = create_res.json()["id"]

    delete_res = client.delete(f"/api/v1/album-formats/{af_id}")

    assert delete_res.status_code == 204
    assert delete_res.content == b""

    # Verify no longer exists
    get_res = client.get(f"/api/v1/album-formats/{af_id}")
    assert get_res.status_code == 404


def test_delete_album_format_not_found(client: TestClient) -> None:
    """Test deleting a non-existent album format returns 404 Not Found.

    Assigned developer: Dev5 (TASK-20)
    """
    response = client.delete("/api/v1/album-formats/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Album format not found"


def test_create_album_format_duplicate_unique_constraint(
    client: TestClient, setup_parents: dict
) -> None:
    """Test duplicate assignment in the same branch violates uq_album_format_branch (400 Bad Request).

    Assigned developer: Dev5 (TASK-20)
    """
    payload = {
        "album_id": setup_parents["album"].id,
        "format_id": setup_parents["format"].id,
        "branch_id": setup_parents["branch"].id,
        "price": 25.0,
        "stock": 10,
    }
    first_res = client.post("/api/v1/album-formats/", json=payload)
    assert first_res.status_code == 201

    duplicate_res = client.post("/api/v1/album-formats/", json=payload)
    assert duplicate_res.status_code == 400
    assert "detail" in duplicate_res.json()


def test_create_album_format_negative_stock_validation(
    client: TestClient, setup_parents: dict
) -> None:
    """Test negative stock triggers validation error (422 Unprocessable Entity).

    Assigned developer: Dev5 (TASK-20)
    """
    payload = {
        "album_id": setup_parents["album"].id,
        "format_id": setup_parents["format"].id,
        "branch_id": setup_parents["branch"].id,
        "price": 25.0,
        "stock": -1,
    }
    response = client.post("/api/v1/album-formats/", json=payload)

    assert response.status_code == 422


def test_create_album_format_negative_price_validation(
    client: TestClient, setup_parents: dict
) -> None:
    """Test negative price triggers validation error (422 Unprocessable Entity).

    Assigned developer: Dev5 (TASK-20)
    """
    payload = {
        "album_id": setup_parents["album"].id,
        "format_id": setup_parents["format"].id,
        "branch_id": setup_parents["branch"].id,
        "price": -10.0,
        "stock": 5,
    }
    response = client.post("/api/v1/album-formats/", json=payload)

    assert response.status_code == 422


def test_create_album_format_invalid_foreign_keys(
    client: TestClient, setup_parents: dict
) -> None:
    """Test non-existent relational parent IDs trigger 404 Not Found.

    Assigned developer: Dev5 (TASK-20)
    """
    # Non-existent album
    res_album = client.post(
        "/api/v1/album-formats/",
        json={
            "album_id": 99999,
            "format_id": setup_parents["format"].id,
            "branch_id": setup_parents["branch"].id,
            "price": 20.0,
            "stock": 5,
        },
    )
    assert res_album.status_code == 404

    # Non-existent format
    res_fmt = client.post(
        "/api/v1/album-formats/",
        json={
            "album_id": setup_parents["album"].id,
            "format_id": 99999,
            "branch_id": setup_parents["branch"].id,
            "price": 20.0,
            "stock": 5,
        },
    )
    assert res_fmt.status_code == 404

    # Non-existent branch
    res_br = client.post(
        "/api/v1/album-formats/",
        json={
            "album_id": setup_parents["album"].id,
            "format_id": setup_parents["format"].id,
            "branch_id": 99999,
            "price": 20.0,
            "stock": 5,
        },
    )
    assert res_br.status_code == 404


def test_cascade_delete_on_album_deletion(
    client: TestClient, setup_parents: dict, db_session: Session
) -> None:
    """Test deleting an album cascades to delete its album_format editions automatically.

    Assigned developer: Dev5 (TASK-20)
    """
    create_res = client.post(
        "/api/v1/album-formats/",
        json={
            "album_id": setup_parents["album"].id,
            "format_id": setup_parents["format"].id,
            "branch_id": setup_parents["branch"].id,
            "price": 30.0,
            "stock": 12,
        },
    )
    af_id = create_res.json()["id"]

    # Delete parent Album via database session to verify relational cascade
    album = db_session.get(Album, setup_parents["album"].id)
    db_session.delete(album)
    db_session.commit()

    # Verify associated AlbumFormat was deleted in cascade
    get_af_res = client.get(f"/api/v1/album-formats/{af_id}")
    assert get_af_res.status_code == 404


def test_cascade_delete_on_format_deletion(
    client: TestClient, setup_parents: dict
) -> None:
    """Test deleting a format cascades to delete its album_format editions automatically.

    Assigned developer: Dev5 (TASK-20)
    """
    create_res = client.post(
        "/api/v1/album-formats/",
        json={
            "album_id": setup_parents["album"].id,
            "format_id": setup_parents["format"].id,
            "branch_id": setup_parents["branch"].id,
            "price": 15.0,
            "stock": 7,
        },
    )
    af_id = create_res.json()["id"]

    # Delete parent Format
    del_fmt_res = client.delete(f"/api/v1/formats/{setup_parents['format'].id}")
    assert del_fmt_res.status_code == 204

    # Verify associated AlbumFormat was deleted in cascade
    get_af_res = client.get(f"/api/v1/album-formats/{af_id}")
    assert get_af_res.status_code == 404


def test_cascade_delete_on_branch_deletion(
    client: TestClient, setup_parents: dict
) -> None:
    """Test deleting a branch cascades to delete its album_format editions automatically.

    Assigned developer: Dev5 (TASK-20)
    """
    create_res = client.post(
        "/api/v1/album-formats/",
        json={
            "album_id": setup_parents["album"].id,
            "format_id": setup_parents["format"].id,
            "branch_id": setup_parents["branch"].id,
            "price": 17.50,
            "stock": 4,
        },
    )
    af_id = create_res.json()["id"]

    # Delete parent Branch
    del_br_res = client.delete(f"/api/v1/branches/{setup_parents['branch'].id}")
    assert del_br_res.status_code == 204

    # Verify associated AlbumFormat was deleted in cascade
    get_af_res = client.get(f"/api/v1/album-formats/{af_id}")
    assert get_af_res.status_code == 404


def test_db_check_constraint_direct_negative_stock(
    db_session: Session, setup_parents: dict
) -> None:
    """Test database-level CheckConstraint ck_album_formats_stock_non_negative directly.

    Assigned developer: Dev5 (TASK-20)
    """
    invalid_item = AlbumFormat(
        album_id=setup_parents["album"].id,
        format_id=setup_parents["format"].id,
        branch_id=setup_parents["branch"].id,
        price=15.0,
        stock=-10,
    )
    db_session.add(invalid_item)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_db_check_constraint_direct_negative_price(
    db_session: Session, setup_parents: dict
) -> None:
    """Test database-level CheckConstraint ck_album_formats_price_non_negative directly.

    Assigned developer: Dev5 (TASK-20)
    """
    invalid_item = AlbumFormat(
        album_id=setup_parents["album"].id,
        format_id=setup_parents["format"].id,
        branch_id=setup_parents["branch"].id,
        price=-5.0,
        stock=10,
    )
    db_session.add(invalid_item)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
