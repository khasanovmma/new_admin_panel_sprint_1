import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass, field

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from .tables import Genre, Person, Filmwork, PersonFilmwork, GenreFilmwork


TABLES = [Genre, Person, Filmwork, PersonFilmwork, GenreFilmwork]

db_path = "db.sqlite"


class SQLiteExtractor:
    QUERIES = {
        Genre.__name__: "SELECT * FROM genre;",
        Person.__name__: "SELECT id, full_name FROM person",
        Filmwork.__name__: ("SELECT * FROM film_work;"),
        PersonFilmwork.__name__: ("SELECT * FROM person_film_work;"),
        GenreFilmwork.__name__: ("SELECT * FROM genre_film_work;"),
    }

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.cursor = self.connection.cursor()

    def extract_movies(self):
        pass


class PostgresSaver:
    def __init__(self, connection: _connection) -> None:
        self.connection = connection
        self.cursor = self.connection.cursor()

    def save_all_data(self, data, table):
        pass


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    data = sqlite_extractor.extract_movies()
    postgres_saver.save_all_data(data)


if __name__ == "__main__":
    dsl = {
        "dbname": "movies_database",
        "user": "root",
        "password": "root",
        "host": "127.0.0.1",
        "port": 5432,
    }
    with sqlite3.connect(db_path) as sqlite_conn, psycopg2.connect(
        **dsl, cursor_factory=DictCursor
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
