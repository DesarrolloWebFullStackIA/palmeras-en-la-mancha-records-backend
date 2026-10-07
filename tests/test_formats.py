from app.models.album import Album
from app.models.album_format import AlbumFormat
from app.models.branch import Branch
from app.models.format import Format


def test_list_formats_empty(client):
    response = client.get("/formats/")

    assert response.status_code == 200
    assert response.json() == []


def test_create_format(client):
    response = client.post(
        "/formats/",
        json={"name": "Vinyl", "description": "12-inch records"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Vinyl"
    assert body["description"] == "12-inch records"
    assert body["albums"] == []


def test_get_update_delete_format(client):
    created = client.post("/formats/", json={"name": "CD"}).json()

    fetched = client.get(f"/formats/{created['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == created["id"]

    updated = client.put(
        f"/formats/{created['id']}",
        json={"description": "Compact disc"},
    )
    assert updated.status_code == 200
    assert updated.json()["description"] == "Compact disc"
    assert updated.json()["name"] == "CD"

    deleted = client.delete(f"/formats/{created['id']}")
    assert deleted.status_code == 200

    missing = client.get(f"/formats/{created['id']}")
    assert missing.status_code == 404


def test_include_albums_and_label_filter(client, db_session):
    label_response = client.post(
        "/record_labels/",
        json={"name": "Blue Note", "country": "United States"},
    )
    label_id = label_response.json()["id"]

    branch = Branch(
        name="Palmeras Madrid",
        address="Calle Mayor 1",
        phone="910000001",
    )
    vinyl = Format(name="Vinyl")
    db_session.add_all([branch, vinyl])
    db_session.flush()

    album = Album(
        title="Kind of Blue",
        artist="Miles Davis",
        release_year=1959,
        label_id=label_id,
    )
    db_session.add(album)
    db_session.flush()

    db_session.add(
        AlbumFormat(
            album_id=album.id,
            format_id=vinyl.id,
            branch_id=branch.id,
            price=25.5,
            stock=5,
        )
    )
    db_session.commit()

    plain = client.get("/formats/").json()
    assert plain[0]["albums"] == []

    nested = client.get("/formats/?include_albums=true").json()
    assert [a["title"] for a in nested[0]["albums"]] == ["Kind of Blue"]

    matching = client.get(f"/formats/?record_label_id={label_id}").json()
    assert [fmt["id"] for fmt in matching] == [vinyl.id]

    without_albums = client.get("/formats/?record_label_id=99999").json()
    assert without_albums == []
