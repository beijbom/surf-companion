from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, create_engine

from config import sqlite_url
from datamodel import Spot, Surfer


def initialize_db() -> None:
    engine = create_engine(sqlite_url)

    bad_surfer = Surfer(name="Farid", email="farid.doe@example.com")
    epic_surfer = Surfer(name="Oscar", email="oscar.doe@example.com")

    spot = Spot(name="Lane")
    good_spot = Spot(name="Natural Bridges")
    try:
        with Session(engine) as session:
            for item in [bad_surfer, epic_surfer, spot, good_spot]:
                try:
                    session.add(item)
                    session.commit()
                except IntegrityError as e:
                    session.rollback()
                    print(f"Skipping duplicate item: {item}")
    except Exception as e:
        print(f"Error during database initialization: {e}")
