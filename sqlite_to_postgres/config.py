from environs import Env

env = Env()
env.read_env()

PG_DATABASE = {
    "dbname": env.str("PG_DB_NAME", "movies_database"),
    "user": env.str("PG_DB_USER"),
    "password": env.str("PG_DB_PASSWORD"),
    "host": env.str("PG_DB_HOST", "127.0.0.1"),
    "port": env.int("PG_DB_PORT", 5432),
}

SQL_DB_PATH = env.str("SQLITE_DB_PATH", "db.sqlite")
