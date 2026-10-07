import time
from typing import Any
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.album import Album
from app.models.album_format import AlbumFormat
from app.models.branch import Branch
from app.models.format import Format
from app.models.record_label import RecordLabel
from app.services.catalog_query import (
    get_catalog_optimized,
    get_catalog_without_optimization,
)


# -----------------------------------------------------------------------------
# TASK-24 (Dev4): Catalog Query Performance Benchmark
# -----------------------------------------------------------------------------

def create_realistic_catalog(
    db_session: Session,
    total_albums: int = 1000,
) -> None:
    """Seed a realistic large catalog for performance benchmarking."""
    labels = [
        RecordLabel(
            name=f"Record Label {index}",
            country="Spain",
            website=None,
        )
        for index in range(20)
    ]

    db_session.add_all(labels)
    db_session.flush()

    albums = [
        Album(
            title=f"Album {index:04d}",
            artist=f"Artist {index % 100}",
            release_year=2000 + (index % 25),
            genre="Indie",
            label_id=labels[index % len(labels)].id,
            cover_image_url=None,
        )
        for index in range(total_albums)
    ]

    db_session.add_all(albums)
    db_session.commit()


def test_catalog_query_performance(db_session: Session) -> None:
    """Benchmark comparing unoptimized vs optimized catalog query execution times.

    Assigned developer: Dev4 (TASK-24)
    """
    create_realistic_catalog(db_session)

    start_without_optimization = time.perf_counter()
    albums_without_optimization = get_catalog_without_optimization(db_session)
    time_without_optimization = time.perf_counter() - start_without_optimization

    start_optimized = time.perf_counter()
    albums_optimized = get_catalog_optimized(db_session)
    time_optimized = time.perf_counter() - start_optimized

    assert len(albums_without_optimization) == 1000
    assert len(albums_optimized) == 1000
    assert [a.title for a in albums_without_optimization] == [a.title for a in albums_optimized]

    print(f"\nWithout optimization: {time_without_optimization * 1000:.3f} ms")
    print(f"Optimized: {time_optimized * 1000:.3f} ms")


# -----------------------------------------------------------------------------
# TASK-25 (Dev5): Exhaustive Search Filter Test Battery (US05)
# -----------------------------------------------------------------------------

@pytest.fixture
def catalog_dataset(db_session: Session) -> dict[str, Any]:
    """Seed a rich relational catalog covering labels, formats, branches, and albums."""
    # 1. Labels
    label_subpop = RecordLabel(name="Sub Pop", country="United States", website="https://subpop.com")
    label_4ad = RecordLabel(name="4AD", country="United Kingdom", website="https://4ad.com")
    label_mortal = RecordLabel(name="Pequeño Salto Mortal", country="Spain", website=None)
    db_session.add_all([label_subpop, label_4ad, label_mortal])
    db_session.flush()

    # 2. Formats
    fmt_vinyl = Format(name='12" Vinyl', description="12 inch 33 RPM")
    fmt_cd = Format(name="Compact Disc", description="Digital Audio CD")
    fmt_cassette = Format(name="Cassette", description="Magnetic tape")
    db_session.add_all([fmt_vinyl, fmt_cd, fmt_cassette])
    db_session.flush()

    # 3. Branches
    branch_madrid = Branch(name="Palmeras Madrid", address="Calle Mayor 1", phone="+34910000001")
    branch_barcelona = Branch(name="Palmeras Barcelona", address="Carrer de Gràcia 2", phone="+34930000002")
    branch_valencia = Branch(name="Palmeras Valencia", address="Carrer de Colón 3", phone="+34960000003")
    db_session.add_all([branch_madrid, branch_barcelona, branch_valencia])
    db_session.flush()

    # 4. Albums
    album_bleach = Album(
        title="Bleach",
        artist="Nirvana",
        release_year=1989,
        genre="Grunge",
        label_id=label_subpop.id,
    )
    album_nevermind = Album(
        title="Nevermind",
        artist="Nirvana",
        release_year=1991,
        genre="Grunge",
        label_id=label_subpop.id,
    )
    album_mundo = Album(
        title="Un Día en el Mundo",
        artist="Vetusta Morla",
        release_year=2008,
        genre="Indie Rock",
        label_id=label_mortal.id,
    )
    album_mapas = Album(
        title="Mapas",
        artist="Vetusta Morla",
        release_year=2011,
        genre="Indie Rock",
        label_id=label_mortal.id,
    )
    album_surfer = Album(
        title="Surfer Rosa",
        artist="Pixies",
        release_year=1988,
        genre="Alternative Rock",
        label_id=label_4ad.id,
    )
    album_doolittle = Album(
        title="Doolittle",
        artist="Pixies",
        release_year=1989,
        genre="Alternative Rock",
        label_id=label_4ad.id,
    )
    db_session.add_all([
        album_bleach,
        album_nevermind,
        album_mundo,
        album_mapas,
        album_surfer,
        album_doolittle,
    ])
    db_session.flush()

    # 5. Inventory (AlbumFormat entries)
    # Bleach: Madrid (Vinyl), Barcelona (Vinyl, CD)
    inv_bleach_mad_v = AlbumFormat(album_id=album_bleach.id, format_id=fmt_vinyl.id, branch_id=branch_madrid.id, price=22.5, stock=5)
    inv_bleach_bcn_v = AlbumFormat(album_id=album_bleach.id, format_id=fmt_vinyl.id, branch_id=branch_barcelona.id, price=22.5, stock=3)
    inv_bleach_bcn_cd = AlbumFormat(album_id=album_bleach.id, format_id=fmt_cd.id, branch_id=branch_barcelona.id, price=14.0, stock=8)

    # Nevermind: Valencia only (Vinyl)
    inv_never_val_v = AlbumFormat(album_id=album_nevermind.id, format_id=fmt_vinyl.id, branch_id=branch_valencia.id, price=25.0, stock=10)

    # Un Día en el Mundo: Madrid (Vinyl, CD), Barcelona (Vinyl)
    inv_mundo_mad_v = AlbumFormat(album_id=album_mundo.id, format_id=fmt_vinyl.id, branch_id=branch_madrid.id, price=24.0, stock=4)
    inv_mundo_mad_cd = AlbumFormat(album_id=album_mundo.id, format_id=fmt_cd.id, branch_id=branch_madrid.id, price=15.0, stock=6)
    inv_mundo_bcn_v = AlbumFormat(album_id=album_mundo.id, format_id=fmt_vinyl.id, branch_id=branch_barcelona.id, price=24.0, stock=2)

    # Mapas: Madrid (CD), Valencia (Cassette)
    inv_mapas_mad_cd = AlbumFormat(album_id=album_mapas.id, format_id=fmt_cd.id, branch_id=branch_madrid.id, price=16.0, stock=7)
    inv_mapas_val_cas = AlbumFormat(album_id=album_mapas.id, format_id=fmt_cassette.id, branch_id=branch_valencia.id, price=12.0, stock=3)

    # Surfer Rosa: Barcelona (CD)
    inv_surfer_bcn_cd = AlbumFormat(album_id=album_surfer.id, format_id=fmt_cd.id, branch_id=branch_barcelona.id, price=13.5, stock=4)

    # Doolittle: Madrid (Cassette), Barcelona (Cassette)
    inv_doo_mad_cas = AlbumFormat(album_id=album_doolittle.id, format_id=fmt_cassette.id, branch_id=branch_madrid.id, price=11.0, stock=2)
    inv_doo_bcn_cas = AlbumFormat(album_id=album_doolittle.id, format_id=fmt_cassette.id, branch_id=branch_barcelona.id, price=11.0, stock=5)

    db_session.add_all([
        inv_bleach_mad_v,
        inv_bleach_bcn_v,
        inv_bleach_bcn_cd,
        inv_never_val_v,
        inv_mundo_mad_v,
        inv_mundo_mad_cd,
        inv_mundo_bcn_v,
        inv_mapas_mad_cd,
        inv_mapas_val_cas,
        inv_surfer_bcn_cd,
        inv_doo_mad_cas,
        inv_doo_bcn_cas,
    ])
    db_session.commit()

    return {
        "labels": {"subpop": label_subpop, "4ad": label_4ad, "mortal": label_mortal},
        "formats": {"vinyl": fmt_vinyl, "cd": fmt_cd, "cassette": fmt_cassette},
        "branches": {"madrid": branch_madrid, "barcelona": branch_barcelona, "valencia": branch_valencia},
        "albums": {
            "bleach": album_bleach,
            "nevermind": album_nevermind,
            "mundo": album_mundo,
            "mapas": album_mapas,
            "surfer": album_surfer,
            "doolittle": album_doolittle,
        },
    }


def test_get_albums_unfiltered_returns_all(client: TestClient, catalog_dataset: dict[str, Any]) -> None:
    """Test retrieving albums without filters returns all catalog albums.

    Assigned developer: Dev5 (TASK-25)
    """
    response = client.get("/api/v1/albums/")

    assert response.status_code == 200
    titles = [a["title"] for a in response.json()]
    assert len(titles) == 6
    assert "Bleach" in titles
    assert "Un Día en el Mundo" in titles


def test_filter_by_title_case_insensitive_partial(client: TestClient, catalog_dataset: dict[str, Any]) -> None:
    """Test title filter supports case-insensitive and partial text match.

    Assigned developer: Dev5 (TASK-25)
    """
    # Uppercase query against lowercase title
    response_upper = client.get("/api/v1/albums/?title=MUNDO")
    assert response_upper.status_code == 200
    titles_upper = [a["title"] for a in response_upper.json()]
    assert titles_upper == ["Un Día en el Mundo"]

    # Partial substring query
    response_partial = client.get("/api/v1/albums/?title=ea")
    assert response_partial.status_code == 200
    titles_partial = [a["title"] for a in response_partial.json()]
    assert titles_partial == ["Bleach"]


def test_filter_by_artist_case_insensitive_partial(client: TestClient, catalog_dataset: dict[str, Any]) -> None:
    """Test artist filter supports case-insensitive and partial text match.

    Assigned developer: Dev5 (TASK-25)
    """
    # Lowercase query
    response = client.get("/api/v1/albums/?artist=vetusta")
    assert response.status_code == 200
    titles = [a["title"] for a in response.json()]
    assert sorted(titles) == ["Mapas", "Un Día en el Mundo"]

    # Partial match for Pixies
    response_pix = client.get("/api/v1/albums/?artist=PIX")
    assert response_pix.status_code == 200
    titles_pix = [a["title"] for a in response_pix.json()]
    assert sorted(titles_pix) == ["Doolittle", "Surfer Rosa"]


def test_filter_by_label_id_exact(client: TestClient, catalog_dataset: dict[str, Any]) -> None:
    """Test exact foreign key filtering by label_id.

    Assigned developer: Dev5 (TASK-25)
    """
    subpop_id = catalog_dataset["labels"]["subpop"].id
    response = client.get(f"/api/v1/albums/?label_id={subpop_id}")

    assert response.status_code == 200
    titles = [a["title"] for a in response.json()]
    assert sorted(titles) == ["Bleach", "Nevermind"]
    assert all(a["label_id"] == subpop_id for a in response.json())


def test_filter_by_label_name_case_insensitive_partial(client: TestClient, catalog_dataset: dict[str, Any]) -> None:
    """Test label name filter matches related record label text.

    Assigned developer: Dev5 (TASK-25)
    """
    response = client.get("/api/v1/albums/?label_name=salto")

    assert response.status_code == 200
    titles = [a["title"] for a in response.json()]
    assert sorted(titles) == ["Mapas", "Un Día en el Mundo"]
    assert all(a["record_label"]["name"] == "Pequeño Salto Mortal" for a in response.json())


def test_filter_by_format_id(client: TestClient, catalog_dataset: dict[str, Any]) -> None:
    """Test filtering by physical format ID returns only albums stocked in that format.

    Assigned developer: Dev5 (TASK-25)
    """
    cassette_id = catalog_dataset["formats"]["cassette"].id
    response = client.get(f"/api/v1/albums/?format_id={cassette_id}")

    assert response.status_code == 200
    titles = [a["title"] for a in response.json()]
    assert sorted(titles) == ["Doolittle", "Mapas"]


def test_filter_by_format_name_case_insensitive_partial(client: TestClient, catalog_dataset: dict[str, Any]) -> None:
    """Test filtering by format name substring (e.g. 'vinyl').

    Assigned developer: Dev5 (TASK-25)
    """
    response = client.get("/api/v1/albums/?format_name=VINYL")

    assert response.status_code == 200
    titles = [a["title"] for a in response.json()]
    # Bleach, Nevermind, and Un Día en el Mundo have Vinyl editions
    assert sorted(titles) == ["Bleach", "Nevermind", "Un Día en el Mundo"]


def test_filter_by_branch_id(client: TestClient, catalog_dataset: dict[str, Any]) -> None:
    """Test filtering by physical store branch ID returns only available stock.

    Assigned developer: Dev5 (TASK-25)
    """
    valencia_id = catalog_dataset["branches"]["valencia"].id
    response = client.get(f"/api/v1/albums/?branch_id={valencia_id}")

    assert response.status_code == 200
    titles = [a["title"] for a in response.json()]
    assert sorted(titles) == ["Mapas", "Nevermind"]


def test_distinct_results_no_duplicate_albums(client: TestClient, catalog_dataset: dict[str, Any]) -> None:
    """Test that albums with multiple inventory formats in the same branch return distinct results.

    Assigned developer: Dev5 (TASK-25)
    """
    madrid_id = catalog_dataset["branches"]["madrid"].id
    # Un Día en el Mundo has both Vinyl and CD in Madrid
    response = client.get(f"/api/v1/albums/?branch_id={madrid_id}")

    assert response.status_code == 200
    titles = [a["title"] for a in response.json()]
    assert len(titles) == len(set(titles))
    assert titles.count("Un Día en el Mundo") == 1
    assert titles.count("Bleach") == 1


def test_combined_filters_title_and_artist(client: TestClient, catalog_dataset: dict[str, Any]) -> None:
    """Test combined filtering by title and artist.

    Assigned developer: Dev5 (TASK-25)
    """
    response = client.get("/api/v1/albums/?title=mundo&artist=vetusta")

    assert response.status_code == 200
    titles = [a["title"] for a in response.json()]
    assert titles == ["Un Día en el Mundo"]


def test_combined_filters_artist_and_label_name(client: TestClient, catalog_dataset: dict[str, Any]) -> None:
    """Test combined filtering by artist and record label name.

    Assigned developer: Dev5 (TASK-25)
    """
    response = client.get("/api/v1/albums/?artist=nirvana&label_name=sub")

    assert response.status_code == 200
    titles = [a["title"] for a in response.json()]
    assert sorted(titles) == ["Bleach", "Nevermind"]


def test_combined_filters_format_and_branch(client: TestClient, catalog_dataset: dict[str, Any]) -> None:
    """Test combined filtering by physical format and physical branch.

    Assigned developer: Dev5 (TASK-25)
    """
    vinyl_id = catalog_dataset["formats"]["vinyl"].id
    madrid_id = catalog_dataset["branches"]["madrid"].id
    response = client.get(f"/api/v1/albums/?format_id={vinyl_id}&branch_id={madrid_id}")

    assert response.status_code == 200
    titles = [a["title"] for a in response.json()]
    # Bleach and Un Día en el Mundo have vinyl in Madrid
    assert sorted(titles) == ["Bleach", "Un Día en el Mundo"]


def test_combined_filters_artist_format_and_branch(client: TestClient, catalog_dataset: dict[str, Any]) -> None:
    """Test 3-way combined filtering by artist, format name, and branch ID.

    Assigned developer: Dev5 (TASK-25)
    """
    bcn_id = catalog_dataset["branches"]["barcelona"].id
    response = client.get(f"/api/v1/albums/?artist=pixies&format_name=cassette&branch_id={bcn_id}")

    assert response.status_code == 200
    titles = [a["title"] for a in response.json()]
    # Only Doolittle is on cassette in Barcelona
    assert titles == ["Doolittle"]


def test_combined_all_five_filters_simultaneously(client: TestClient, catalog_dataset: dict[str, Any]) -> None:
    """Test simultaneous filtering by title, artist, label, format, and branch.

    Assigned developer: Dev5 (TASK-25)
    """
    subpop_id = catalog_dataset["labels"]["subpop"].id
    vinyl_id = catalog_dataset["formats"]["vinyl"].id
    madrid_id = catalog_dataset["branches"]["madrid"].id

    query = (
        f"/api/v1/albums/"
        f"?title=bleach"
        f"&artist=nirvana"
        f"&label_id={subpop_id}"
        f"&format_id={vinyl_id}"
        f"&branch_id={madrid_id}"
    )
    response = client.get(query)

    assert response.status_code == 200
    titles = [a["title"] for a in response.json()]
    assert titles == ["Bleach"]


def test_combined_filters_no_match_returns_empty_list(client: TestClient, catalog_dataset: dict[str, Any]) -> None:
    """Test that mutually exclusive or non-existent filter combinations return an empty list with 200 OK.

    Assigned developer: Dev5 (TASK-25)
    """
    valencia_id = catalog_dataset["branches"]["valencia"].id
    # Bleach is not stocked in Valencia
    response = client.get(f"/api/v1/albums/?title=Bleach&branch_id={valencia_id}")

    assert response.status_code == 200
    assert response.json() == []


def test_filter_validation_error_invalid_ids(client: TestClient) -> None:
    """Test validation errors (422) when passing IDs <= 0 (gt=0 constraint).

    Assigned developer: Dev5 (TASK-25)
    """
    res_label = client.get("/api/v1/albums/?label_id=0")
    assert res_label.status_code == 422

    res_format = client.get("/api/v1/albums/?format_id=-1")
    assert res_format.status_code == 422

    res_branch = client.get("/api/v1/albums/?branch_id=0")
    assert res_branch.status_code == 422


def test_filter_validation_error_invalid_types(client: TestClient) -> None:
    """Test validation failure (422) for query parameters with incompatible types.

    Assigned developer: Dev5 (TASK-25)
    """
    res_label = client.get("/api/v1/albums/?label_id=not-an-int")
    assert res_label.status_code == 422

    res_format = client.get("/api/v1/albums/?format_id=invalid")
    assert res_format.status_code == 422

    res_branch = client.get("/api/v1/albums/?branch_id=abc")
    assert res_branch.status_code == 422


def test_filtered_pagination_skip_and_limit(client: TestClient, catalog_dataset: dict[str, Any]) -> None:
    """Test pagination parameters skip and limit when filters are applied.

    Assigned developer: Dev5 (TASK-25)
    """
    # Nirvana has 2 albums: Bleach and Nevermind (ordered by title asc)
    response_page1 = client.get("/api/v1/albums/?artist=nirvana&limit=1&skip=0")
    assert response_page1.status_code == 200
    data_page1 = response_page1.json()
    assert len(data_page1) == 1
    assert data_page1[0]["title"] == "Bleach"

    response_page2 = client.get("/api/v1/albums/?artist=nirvana&limit=1&skip=1")
    assert response_page2.status_code == 200
    data_page2 = response_page2.json()
    assert len(data_page2) == 1
    assert data_page2[0]["title"] == "Nevermind"


def test_get_album_by_id_success(client: TestClient, catalog_dataset: dict[str, Any]) -> None:
    """Test retrieving an album by ID returns 200 OK with populated record label.

    Assigned developer: Dev5 (TASK-25)
    """
    album_id = catalog_dataset["albums"]["bleach"].id
    response = client.get(f"/api/v1/albums/{album_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == album_id
    assert data["title"] == "Bleach"
    assert data["artist"] == "Nirvana"
    assert data["record_label"]["name"] == "Sub Pop"


def test_get_album_by_id_not_found(client: TestClient) -> None:
    """Test retrieving a non-existent album returns 404 Not Found.

    Assigned developer: Dev5 (TASK-25)
    """
    response = client.get("/api/v1/albums/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Album not found"