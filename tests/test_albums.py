from io import BytesIO
from unittest.mock import AsyncMock, patch
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.record_label import RecordLabel


@pytest.fixture
def sample_label(db_session: Session) -> RecordLabel:
    """Create and return a sample RecordLabel in the test database for foreign key association."""
    label = RecordLabel(
        name="Sub Pop Records",
        country="United States",
        website="https://www.subpop.com",
    )
    db_session.add(label)
    db_session.commit()
    db_session.refresh(label)
    return label


def test_create_album_with_cover_image_mocked(
    client: TestClient, sample_label: RecordLabel
) -> None:
    """Test creating an album with an image upload, mocking CloudinaryService.upload_image.

    Assigned developer: Dev5 (TASK-15)
    """
    fake_cloudinary_url = "https://res.cloudinary.com/palmeras/image/upload/v1234/bleach_cover.jpg"

    with patch(
        "app.routers.albums.CloudinaryService.upload_image",
        new_callable=AsyncMock,
    ) as mock_upload:
        mock_upload.return_value = fake_cloudinary_url

        image_content = b"fake_jpeg_image_binary_data"
        files = {
            "image": ("bleach.jpg", BytesIO(image_content), "image/jpeg"),
        }
        data = {
            "title": "Bleach",
            "artist": "Nirvana",
            "release_year": 1989,
            "genre": "Grunge",
            "label_id": sample_label.id,
        }

        response = client.post("/api/v1/albums/", data=data, files=files)

        assert response.status_code == 200
        payload = response.json()
        assert payload["id"] is not None
        assert payload["title"] == "Bleach"
        assert payload["artist"] == "Nirvana"
        assert payload["release_year"] == 1989
        assert payload["genre"] == "Grunge"
        assert payload["label_id"] == sample_label.id
        assert payload["cover_image_url"] == fake_cloudinary_url

        mock_upload.assert_awaited_once()


def test_create_album_without_cover_image(
    client: TestClient, sample_label: RecordLabel
) -> None:
    """Test creating an album without uploading an image.

    Assigned developer: Dev5 (TASK-15)
    """
    data = {
        "title": "Nevermind",
        "artist": "Nirvana",
        "release_year": 1991,
        "genre": "Grunge",
        "label_id": sample_label.id,
    }

    response = client.post("/api/v1/albums/", data=data)

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] is not None
    assert payload["title"] == "Nevermind"
    assert payload["artist"] == "Nirvana"
    assert payload["release_year"] == 1991
    assert payload["genre"] == "Grunge"
    assert payload["label_id"] == sample_label.id
    assert payload["cover_image_url"] is None


def test_create_album_missing_required_fields(client: TestClient) -> None:
    """Test validation failure (422) when required fields are missing.

    Assigned developer: Dev5 (TASK-15)
    """
    # Missing artist, release_year, and label_id
    data = {
        "title": "In Utero",
    }

    response = client.post("/api/v1/albums/", data=data)

    assert response.status_code == 422


def test_create_album_invalid_foreign_key(client: TestClient) -> None:
    """Test that creating an album with a nonexistent label_id triggers relational error handling (404).

    Assigned developer: Dev5 (TASK-15)
    """
    data = {
        "title": "Unknown Album",
        "artist": "Unknown Artist",
        "release_year": 2020,
        "genre": "Indie",
        "label_id": 99999,
    }

    response = client.post("/api/v1/albums/", data=data)

    assert response.status_code == 404
    payload = response.json()
    assert "detail" in payload


def test_update_album_metadata_without_image(
    client: TestClient, sample_label: RecordLabel
) -> None:
    """Test updating existing album metadata without modifying the cover image.

    Assigned developer: Dev5 (TASK-15)
    """
    create_data = {
        "title": "In Utero",
        "artist": "Nirvana",
        "release_year": 1993,
        "genre": "Grunge",
        "label_id": sample_label.id,
    }
    create_response = client.post("/api/v1/albums/", data=create_data)
    assert create_response.status_code == 200
    album_id = create_response.json()["id"]

    update_data = {
        "title": "In Utero (Deluxe 30th Anniversary)",
        "artist": "Nirvana",
        "release_year": 2023,
        "genre": "Grunge / Rock",
        "label_id": sample_label.id,
    }
    update_response = client.put(f"/api/v1/albums/{album_id}", data=update_data)

    assert update_response.status_code == 200
    updated_payload = update_response.json()
    assert updated_payload["id"] == album_id
    assert updated_payload["title"] == "In Utero (Deluxe 30th Anniversary)"
    assert updated_payload["release_year"] == 2023
    assert updated_payload["genre"] == "Grunge / Rock"


def test_update_album_with_new_cover_image_mocked(
    client: TestClient, sample_label: RecordLabel
) -> None:
    """Test updating an existing album with a new cover image, mocking CloudinaryService.upload_image.

    Assigned developer: Dev5 (TASK-15)
    """
    create_data = {
        "title": "Incesticide",
        "artist": "Nirvana",
        "release_year": 1992,
        "genre": "Grunge",
        "label_id": sample_label.id,
    }
    create_response = client.post("/api/v1/albums/", data=create_data)
    assert create_response.status_code == 200
    album_id = create_response.json()["id"]

    updated_cloudinary_url = "https://res.cloudinary.com/palmeras/image/upload/v5678/new_incesticide.png"

    with patch(
        "app.routers.albums.CloudinaryService.upload_image",
        new_callable=AsyncMock,
    ) as mock_upload:
        mock_upload.return_value = updated_cloudinary_url

        files = {
            "image": ("incesticide_new.png", BytesIO(b"new_png_data"), "image/png"),
        }
        update_data = {
            "title": "Incesticide (Remastered)",
            "artist": "Nirvana",
            "release_year": 1992,
            "genre": "Grunge",
            "label_id": sample_label.id,
        }

        update_response = client.put(
            f"/api/v1/albums/{album_id}",
            data=update_data,
            files=files,
        )

        assert update_response.status_code == 200
        payload = update_response.json()
        assert payload["id"] == album_id
        assert payload["title"] == "Incesticide (Remastered)"
        assert payload["cover_image_url"] == updated_cloudinary_url

        mock_upload.assert_awaited_once()


def test_update_album_not_found(client: TestClient) -> None:
    """Test updating a non-existent album returns 404 Not Found.

    Assigned developer: Dev5 (TASK-15)
    """
    update_data = {
        "title": "Ghost Album",
        "artist": "Ghost Artist",
        "release_year": 2024,
    }

    response = client.put("/api/v1/albums/99999", data=update_data)

    assert response.status_code == 404
    payload = response.json()
    assert payload["detail"] == "Album not found"
