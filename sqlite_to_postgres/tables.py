from uuid import UUID, uuid4
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Literal, Optional
import sqlite3


@dataclass
class UUIDMixin:
    id: UUID = field(default_factory=uuid4)


@dataclass
class TimeStampedMixin:
    created: field(default=None)
    modified: field(default=None)


@dataclass
class Filmwork(UUIDMixin, TimeStampedMixin):
    title: str = field(default="")
    description: str = field(default="")
    creation_date: Optional[date] = field(default="")
    type: Literal["movie", "tv show"] = field(default="movie")
    certificate: Optional[str] = field(default="")
    file_path: Optional[str] = field(default="")
    rating: float = field(default=0.0)


@dataclass
class Genre(UUIDMixin):
    name: str = field(default="")
    description: Optional[str] = field(default="")


@dataclass
class GenreFilmwork(UUIDMixin):
    film_work_id: UUID = field(default_factory=uuid4)
    genre_id: UUID = field(default_factory=uuid4)
    created: Optional[datetime] = field(default=None)


@dataclass
class Person(UUIDMixin, TimeStampedMixin):
    full_name: str = field(default="")
    film_work_id: UUID = field(default_factory=uuid4)


@dataclass
class PersonFilmwork(UUIDMixin):
    film_work_id: UUID = field(default_factory=uuid4)
    person_id: UUID = field(default_factory=uuid4)
    role: Literal["actor", "director", "witer"] = field(default="actor")
    created: Optional[datetime] = field(default=None)


TABLES = [Genre, Person, Filmwork, PersonFilmwork, GenreFilmwork]
