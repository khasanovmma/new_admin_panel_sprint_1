-- Схема 'content'
CREATE SCHEMA IF NOT EXISTS content;

-- Таблица 'Кинопроизведения'
CREATE TABLE IF NOT EXISTS content.film_work (
	id uuid PRIMARY KEY,
	title TEXT NOT NULL,
	description TEXT,
	rating FLOAT,
	creation_date timestamp with time zone, 
	type TEXT not null,
	file_path TEXT,
	created_at timestamp with time zone,
	updated_at timestamp with time zone);

-- Таблица 'Жанры'
CREATE TABLE IF NOT EXISTS content.genre (
	id uuid PRIMARY KEY,
	name TEXT NOT NULL,
	description TEXT,
	created_at timestamp with time zone,
	updated_at timestamp with time zone);

-- 'Персонажи'
CREATE TABLE IF NOT EXISTS content.person (
	id uuid PRIMARY KEY,
	full_name TEXT NOT NULL,
	created_at timestamp with time zone,
	updated_at timestamp with time zone);

-- 'Персонажи фильма'
CREATE TABLE IF NOT EXISTS content.person_film_work (
	id uuid PRIMARY KEY,
	person_id uuid REFERENCES content.person (id),
	film_work_id uuid REFERENCES content.film_work (id),
	role TEXT NOT NULL,
	created_at timestamp with time zone);

-- 'Жанры фильма'
CREATE TABLE IF NOT EXISTS content.genre_film_work (
	id uuid PRIMARY KEY,
	genre_id uuid REFERENCES content.genre (id),
	film_work_id uuid REFERENCES content.film_work (id),
	created_at timestamp with time zone);

CREATE INDEX film_work_creation_date_idx ON content.film_work(creation_date);
CREATE UNIQUE INDEX film_work_person_idx ON content.person_film_work (film_work_id, person_id, role);
CREATE UNIQUE INDEX IF NOT EXISTS genre_name_idx ON content.genre (name);
CREATE UNIQUE INDEX IF NOT EXISTS person_full_name_idx ON content.person (full_name);
CREATE UNIQUE INDEX IF NOT EXISTS film_work_genre_idx ON content.genre_film_work (film_work_id, genre_id);