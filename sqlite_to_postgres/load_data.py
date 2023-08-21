import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass, field, fields, asdict, astuple

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from tables import Genre, Person, Filmwork, PersonFilmwork, GenreFilmwork


TABLES = [Genre, Person, Filmwork, PersonFilmwork, GenreFilmwork]

db_path = "db.sqlite"


class SQLiteExtractor:
    TABLE_MAP = {
        "genre": Genre,
        "person": Person,
        "film_work": Filmwork,
        "person_film_work": PersonFilmwork,
        "genre_film_work": GenreFilmwork,
    }
    FETCH_SIZE = 100

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.cursor.row_factory = sqlite3.Row

    def extract_movies(self):
        movies = {}
        for table_name, model_class in self.TABLE_MAP.items():
            self.cursor.execute(f"SELECT * FROM {table_name};")
            batches: list[model_class] = []
            while data := self.cursor.fetchmany(self.FETCH_SIZE):
                converted_data = [model_class(**movie) for movie in data]
                batches.extend(converted_data)
            movies[table_name] = batches
        return movies

class PostgresSaver:
    def __init__(self, connection: _connection) -> None:
        self.connection = connection
        self.cursor = self.connection.cursor()

    def save_all_data(self, data):
        for table_name, instances in data.items():
            self.clear_database(table_name=table_name)
            column_names = [field.name for field in fields(instances[0])]
            column_count = ', '.join(['%s'] * len(column_names))
            bind_values = ','.join(self.cursor.mogrify(f"({column_count})", row).decode('utf-8') for row in astuple())
    
    def clear_database(self, table_name):
        self.cursor.execute(f"TRUNCATE content.{table_name};")

    
    def get_column_names(self, instances):
        return [field.name for field in fields(instances)]
    



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
