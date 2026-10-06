import time

from app.models.album import Album
from app.models.record_label import RecordLabel
from app.services.catalog_query import (
    get_catalog_optimized,
    get_catalog_without_optimization,
)


def create_realistic_catalog(
    db_session,
    total_albums: int = 1000,
):
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


def test_catalog_query_performance(db_session):
    create_realistic_catalog(db_session)

    start_without_optimization = time.perf_counter()

    albums_without_optimization = get_catalog_without_optimization(
        db_session
    )

    time_without_optimization = (
        time.perf_counter() - start_without_optimization
    )

    start_optimized = time.perf_counter()

    albums_optimized = get_catalog_optimized(db_session)

    time_optimized = time.perf_counter() - start_optimized

    assert len(albums_without_optimization) == 1000
    assert len(albums_optimized) == 1000

    assert [
        album.title for album in albums_without_optimization
    ] == [
        album.title for album in albums_optimized
    ]

    print(
        f"\nWithout optimization: "
        f"{time_without_optimization * 1000:.3f} ms"
    )

    print(
        f"Optimized: "
        f"{time_optimized * 1000:.3f} ms"
    )