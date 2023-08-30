import sqlite3
from datetime import datetime
from contextlib import contextmanager, closing
from dataclasses import fields, astuple

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from tables import Genre, Person, Filmwork, PersonFilmwork, GenreFilmwork

from config import SQL_DB_PATH, PG_DATABASE


class SQLiteExtractor:
    FETCH_SIZE = 100

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def extract_movies(self, table, model):
        curs = self.connection.cursor()
        curs.row_factory = sqlite3.Row
        curs.execute(f"SELECT * FROM {table};")
        while records := curs.fetchmany(self.FETCH_SIZE):
            yield [model(**dict(record)) for record in records]


class PostgresSaver:
    def __init__(self, connection: _connection):
        self.conn = connection

    def save_all_data(self, table, model, rows):
        with self.conn.cursor() as curs:
            column_names = ", ".join(field.name for field in fields(model))
            template = ", ".join(["%s"] * len(fields(model)))
            for row in rows:
                res = curs.mogrify(f"({template})", astuple(row)).decode("utf-8")
                query = f"""
                    INSERT INTO content.{table} ({column_names}) VALUES {res} ON CONFLICT (id) DO NOTHING;
                """
                curs.execute(query)
            self.conn.commit()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)
    TABLE_MAP = {
        "film_work": Filmwork,
        "genre": Genre,
        "person": Person,
        "person_film_work": PersonFilmwork,
        "genre_film_work": GenreFilmwork,
    }

    for table, model in TABLE_MAP.items():
        for rows in sqlite_extractor.extract_movies(table=table, model=model):
            postgres_saver.save_all_data(table=table, model=model, rows=rows)


@contextmanager
def conn_context(db_path: str):
    sqlite3.register_converter(
        "timestamp", lambda x: datetime.fromisoformat(x.decode() + ":00")
    )
    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    yield conn
    conn.close()


if __name__ == "__main__":
    with conn_context(SQL_DB_PATH) as sqlite_conn, closing(
        psycopg2.connect(**PG_DATABASE, cursor_factory=DictCursor)
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
