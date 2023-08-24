from uuid import UUID, uuid4
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, date, timezone
from typing import Literal, Optional
import sqlite3


@dataclass
class UUIDMixin:
    id: UUID = field(default=None)


@dataclass
class CreatedAtMixin:
    created_at: field(default=None)


@dataclass
class UpdatedAtMixin:
    updated_at: field(default=None)


@dataclass
class TimeStampedMixin(CreatedAtMixin, UpdatedAtMixin):
    pass


@dataclass
class Filmwork(UUIDMixin, TimeStampedMixin):
    title: str = field(default="")
    description: str = field(default="")
    creation_date: Optional[date] = field(default="")
    type: Literal["movie", "tv show"] = field(default="movie")
    file_path: Optional[str] = field(default=None)
    rating: float = field(default=0.0)


@dataclass
class Genre(UUIDMixin, TimeStampedMixin):
    name: str = field(default="")
    description: Optional[str] = field(default="")


@dataclass
class GenreFilmwork(UUIDMixin, CreatedAtMixin):
    film_work_id: UUID = field(default_factory=uuid4)
    genre_id: UUID = field(default_factory=uuid4)


@dataclass
class Person(UUIDMixin, TimeStampedMixin):
    full_name: str = field(default="")


@dataclass
class PersonFilmwork(UUIDMixin, CreatedAtMixin):
    film_work_id: UUID = field(default_factory=uuid4)
    person_id: UUID = field(default_factory=uuid4)
    role: Literal["actor", "director", "witer"] = field(default="actor")


TABLES = [Genre, Person, Filmwork, PersonFilmwork, GenreFilmwork]
