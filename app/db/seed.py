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

        print("Seeding database with Palmeras en la Mancha & Nano Banana catalog...")

        # 1. Labels
        palmeras = RecordLabel(name="Palmeras Records", country="Spain", website="https://palmeras-records.es")
        mancha_sound = RecordLabel(name="La Mancha Sound", country="Spain", website="https://lamanchasound.com")
        discos_rad = RecordLabel(name="Discos Radiactivos", country="Spain", website="https://discosradiactivos.com")
        sub_pop = RecordLabel(name="Sub Pop", country="United States", website="https://subpop.com")
        four_ad = RecordLabel(name="4AD", country="United Kingdom", website="https://4ad.com")
        db.add_all([palmeras, mancha_sound, discos_rad, sub_pop, four_ad])
        db.flush()

        # 2. Formats
        vinyl_lp = Format(name='12" LP Vinyl', description="12 inch 33 RPM standard vinyl")
        vinyl_single = Format(name='7" Single Vinyl', description="7 inch 45 RPM vinyl single")
        vinyl_ep = Format(name='10" EP Collector Vinyl', description="10 inch collector edition vinyl")
        cassette = Format(name="Cassette Tape", description="High-fidelity magnetic audio cassette")
        deluxe_box = Format(name="Deluxe Box Set", description="Double vinyl box set with art book")
        db.add_all([vinyl_lp, vinyl_single, vinyl_ep, cassette, deluxe_box])
        db.flush()

        # 3. Branches (Castilla-La Mancha Regional Hub)
        toledo = Branch(name="Sucursal Central - Toledo", address="Calle Comercio 12, Toledo", phone="+34925112233")
        albacete = Branch(name="Filial Albacete", address="Calle Mayor 45, Albacete", phone="+34967445566")
        ciudad_real = Branch(name="Filial Ciudad Real", address="Plaza Mayor 8, Ciudad Real", phone="+34926778899")
        cuenca = Branch(name="Filial Cuenca", address="Calle Carretería 19, Cuenca", phone="+34969332211")
        guadalajara = Branch(name="Filial Guadalajara", address="Calle Mayor 3, Guadalajara", phone="+34949556677")
        db.add_all([toledo, albacete, ciudad_real, cuenca, guadalajara])
        db.flush()

        # 4. Albums with Nano Banana & indie covers hosted on Cloudinary
        nano_groove = Album(
            title="Nano Banana Groove",
            artist="Nano Banana & The Palms",
            release_year=2024,
            genre="Tropical Indie",
            label_id=palmeras.id,
            cover_image_url="https://res.cloudinary.com/e68qv0dz/image/upload/v1791449991/palmeras_records_covers/ldq5hmytmo5oyjw6qrti.jpg",
        )
        banana_split = Album(
            title="Banana Split Sessions",
            artist="Nano Banana",
            release_year=2025,
            genre="Lo-Fi City Pop",
            label_id=palmeras.id,
            cover_image_url="https://res.cloudinary.com/e68qv0dz/image/upload/v1791449992/palmeras_records_covers/b7c4oikek2ggh6wqpibm.jpg",
        )
        cosecha = Album(
            title="Cosecha Eléctrica",
            artist="Los Molinos Sonoros",
            release_year=2023,
            genre="Psychedelic Rock",
            label_id=mancha_sound.id,
            cover_image_url="https://res.cloudinary.com/e68qv0dz/image/upload/v1791449993/palmeras_records_covers/auy6bwpexsrcz30httdy.jpg",
        )
        viento = Album(
            title="Viento de Levante & Silencios",
            artist="Clara & Los Vientos",
            release_year=2022,
            genre="Indie Folk",
            label_id=mancha_sound.id,
        )
        molinos_neon = Album(
            title="Molinos y Neón",
            artist="Cervantes Synth Club",
            release_year=2024,
            genre="Synthwave",
            label_id=discos_rad.id,
        )
        db.add_all([nano_groove, banana_split, cosecha, viento, molinos_neon])
        db.flush()

        # 5. Inventory
        stock_items = [
            AlbumFormat(album_id=nano_groove.id, format_id=vinyl_lp.id, branch_id=toledo.id, price=24.99, stock=18),
            AlbumFormat(album_id=nano_groove.id, format_id=vinyl_lp.id, branch_id=albacete.id, price=24.99, stock=12),
            AlbumFormat(album_id=nano_groove.id, format_id=vinyl_single.id, branch_id=ciudad_real.id, price=14.50, stock=25),
            AlbumFormat(album_id=nano_groove.id, format_id=deluxe_box.id, branch_id=toledo.id, price=49.99, stock=5),
            AlbumFormat(album_id=banana_split.id, format_id=vinyl_lp.id, branch_id=toledo.id, price=23.50, stock=15),
            AlbumFormat(album_id=banana_split.id, format_id=cassette.id, branch_id=albacete.id, price=12.00, stock=20),
            AlbumFormat(album_id=banana_split.id, format_id=vinyl_ep.id, branch_id=cuenca.id, price=19.99, stock=8),
            AlbumFormat(album_id=cosecha.id, format_id=vinyl_lp.id, branch_id=toledo.id, price=25.00, stock=14),
            AlbumFormat(album_id=cosecha.id, format_id=vinyl_lp.id, branch_id=ciudad_real.id, price=25.00, stock=10),
            AlbumFormat(album_id=viento.id, format_id=vinyl_lp.id, branch_id=toledo.id, price=21.99, stock=9),
            AlbumFormat(album_id=viento.id, format_id=cassette.id, branch_id=guadalajara.id, price=11.50, stock=16),
            AlbumFormat(album_id=molinos_neon.id, format_id=vinyl_lp.id, branch_id=toledo.id, price=26.00, stock=11),
            AlbumFormat(album_id=molinos_neon.id, format_id=deluxe_box.id, branch_id=albacete.id, price=52.00, stock=4),
        ]
        db.add_all(stock_items)
        db.commit()

        print(f"Successfully seeded {len(stock_items)} inventory items across {len(db.query(Album).all())} albums!")
    except Exception as exc:
        db.rollback()
        print(f"Error seeding database: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
