from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, create_engine

from config import sqlite_url
from datamodel import Spot, Surfer


def initialize_db() -> None:
    engine = create_engine(sqlite_url)

    bad_surfer = Surfer(name="Farid", email="farid.doe@example.com")
    epic_surfer = Surfer(name="Oscar", email="oscar.doe@example.com")

    spot = Spot(name="Lane")
    try:
        with Session(engine) as session:
            session.add_all([bad_surfer, epic_surfer, spot])
            session.commit()
    except IntegrityError as e:
        session.rollback()
        print("Warning: Some entries were skipped due to duplicates")
    except Exception as e:
        session.rollback()
        print(f"Error during database initialization: {e}")
