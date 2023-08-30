from uuid import UUID
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Literal, Optional


@dataclass
class UUIDMixin:
    id: UUID


@dataclass
class CreatedAtMixin:
    created_at: datetime


@dataclass
class UpdatedAtMixin:
    updated_at: datetime


@dataclass
class TimeStampedMixin(CreatedAtMixin, UpdatedAtMixin):
    pass


@dataclass
class Filmwork(UUIDMixin, TimeStampedMixin):
    title: str = field(default="")
    description: str = field(default="")
    creation_date: Optional[date] = field(default=None)
    type: Literal["movie", "tv show"] = field(default="movie")
    file_path: Optional[str] = field(default=None)
    rating: float = field(default=0.0)


@dataclass
class Genre(UUIDMixin, TimeStampedMixin):
    name: str = field(default="")
    description: Optional[str] = field(default="")


@dataclass
class GenreFilmwork(UUIDMixin, CreatedAtMixin):
    film_work_id: UUID = field()
    genre_id: UUID = field()


@dataclass
class Person(UUIDMixin, TimeStampedMixin):
    full_name: str = field(default="")


@dataclass
class PersonFilmwork(UUIDMixin, CreatedAtMixin):
    film_work_id: UUID = field()
    person_id: UUID = field()
    role: Literal["actor", "director", "witer"] = field(default="actor")


TABLES = [Genre, Person, Filmwork, PersonFilmwork, GenreFilmwork]
