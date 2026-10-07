"""Database seeding script for Palmeras en la Mancha Records.

Usage:
    python -m app.db.seed
"""

from app.core.database import Base, SessionLocal, engine
from app.models.album import Album
from app.models.album_format import AlbumFormat
from app.models.branch import Branch
from app.models.format import Format
from app.models.record_label import RecordLabel


def seed_database() -> None:
    """Populate the database with realistic indie music catalog and inventory data."""
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check idempotency
        if db.query(Album).first() is not None:
            print("Database already contains records. Skipping seed.")
            return

        print("Seeding database with indie catalog...")

        # 1. Labels
        sub_pop = RecordLabel(name="Sub Pop", country="United States", website="https://subpop.com")
        four_ad = RecordLabel(name="4AD", country="United Kingdom", website="https://4ad.com")
        mortal = RecordLabel(name="Pequeño Salto Mortal", country="Spain", website=None)
        matador = RecordLabel(name="Matador Records", country="United States", website="https://matadorrecords.com")
        db.add_all([sub_pop, four_ad, mortal, matador])
        db.flush()

        # 2. Formats
        vinyl = Format(name='12" Vinyl', description="12 inch 33 RPM standard vinyl")
        cd = Format(name="Compact Disc", description="Standard audio CD jewel case")
        cassette = Format(name="Cassette", description="Magnetic audio cassette tape")
        db.add_all([vinyl, cd, cassette])
        db.flush()

        # 3. Branches
        madrid = Branch(name="Palmeras Madrid Central", address="Calle del Pez 21, Malasaña", phone="+34912345678")
        barcelona = Branch(name="Palmeras Barcelona Gràcia", address="Carrer de Verdi 14, Gràcia", phone="+34934567890")
        valencia = Branch(name="Palmeras Valencia Ruzafa", address="Carrer de Cuba 8, Ruzafa", phone="+34963456789")
        db.add_all([madrid, barcelona, valencia])
        db.flush()

        # 4. Albums
        bleach = Album(
            title="Bleach",
            artist="Nirvana",
            release_year=1989,
            genre="Grunge",
            label_id=sub_pop.id,
            cover_image_url="https://res.cloudinary.com/demo/image/upload/bleach.jpg",
        )
        nevermind = Album(
            title="Nevermind",
            artist="Nirvana",
            release_year=1991,
            genre="Grunge",
            label_id=sub_pop.id,
        )
        mundo = Album(
            title="Un Día en el Mundo",
            artist="Vetusta Morla",
            release_year=2008,
            genre="Indie Rock",
            label_id=mortal.id,
        )
        mapas = Album(
            title="Mapas",
            artist="Vetusta Morla",
            release_year=2011,
            genre="Indie Rock",
            label_id=mortal.id,
        )
        surfer = Album(
            title="Surfer Rosa",
            artist="Pixies",
            release_year=1988,
            genre="Alternative Rock",
            label_id=four_ad.id,
        )
        doolittle = Album(
            title="Doolittle",
            artist="Pixies",
            release_year=1989,
            genre="Alternative Rock",
            label_id=four_ad.id,
        )
        db.add_all([bleach, nevermind, mundo, mapas, surfer, doolittle])
        db.flush()

        # 5. Inventory
        stock_items = [
            AlbumFormat(album_id=bleach.id, format_id=vinyl.id, branch_id=madrid.id, price=23.99, stock=8),
            AlbumFormat(album_id=bleach.id, format_id=vinyl.id, branch_id=barcelona.id, price=23.99, stock=5),
            AlbumFormat(album_id=bleach.id, format_id=cd.id, branch_id=barcelona.id, price=14.99, stock=12),
            AlbumFormat(album_id=nevermind.id, format_id=vinyl.id, branch_id=valencia.id, price=25.99, stock=10),
            AlbumFormat(album_id=mundo.id, format_id=vinyl.id, branch_id=madrid.id, price=24.50, stock=6),
            AlbumFormat(album_id=mundo.id, format_id=cd.id, branch_id=madrid.id, price=15.00, stock=10),
            AlbumFormat(album_id=mundo.id, format_id=vinyl.id, branch_id=barcelona.id, price=24.50, stock=4),
            AlbumFormat(album_id=mapas.id, format_id=cd.id, branch_id=madrid.id, price=15.00, stock=7),
            AlbumFormat(album_id=mapas.id, format_id=cassette.id, branch_id=valencia.id, price=12.50, stock=3),
            AlbumFormat(album_id=surfer.id, format_id=cd.id, branch_id=barcelona.id, price=13.99, stock=9),
            AlbumFormat(album_id=doolittle.id, format_id=cassette.id, branch_id=madrid.id, price=11.99, stock=4),
            AlbumFormat(album_id=doolittle.id, format_id=cassette.id, branch_id=barcelona.id, price=11.99, stock=6),
        ]
        db.add_all(stock_items)
        db.commit()

        print(f"Successfully seeded {len(stock_items)} inventory items across 6 albums!")
    except Exception as exc:
        db.rollback()
        print(f"Error seeding database: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
