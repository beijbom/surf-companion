import enum
from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlalchemy import UniqueConstraint, create_engine, text
from sqlalchemy.orm import Session
from sqlmodel import Column, Enum, Field, SQLModel

from config import sqlite_url


class Rating(int, enum.Enum):
    AWFUL = 1
    BAD = 2
    GOOD = 3
    GREAT = 4
    EPIC = 5


class Surfer(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("name", "email", name="unique_name_email"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: EmailStr


class Spot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    image_path: Optional[str] = None
    description: Optional[str] = None


class SurfSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now)
    crowd: Optional[Rating] = None
    wind: Optional[Rating] = None
    waves: Optional[Rating] = None
    surfer_id: Optional[int] = Field(default=None, foreign_key="surfer.id")
    spot_id: Optional[int] = Field(default=None, foreign_key="spot.id")


def add_latitude_longitude_columns() -> None:
    engine = create_engine(sqlite_url)
    with Session(engine) as session:
        for column_def in [
            ("latitude", "FLOAT"),
            ("longitude", "FLOAT"),
            ("image_path", "TEXT"),
            ("description", "TEXT"),
        ]:
            try:
                session.execute(text(f"ALTER TABLE spot ADD COLUMN {column_def[0]} {column_def[1]}"))
            except Exception as e:
                # Column might already exist, skip
                print(f"Skipping {column_def[0]}: {str(e)}")
        session.commit()


# Add this call before any database operations
