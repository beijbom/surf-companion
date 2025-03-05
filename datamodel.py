import enum
from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlalchemy import UniqueConstraint
from sqlmodel import Column, Enum, Field, SQLModel


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


class SurfSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now)
    crowd: Optional[Rating] = None
    wind: Optional[Rating] = None
    waves: Optional[Rating] = None
    surfer_id: Optional[int] = Field(default=None, foreign_key="surfer.id")
    spot_id: Optional[int] = Field(default=None, foreign_key="spot.id")
