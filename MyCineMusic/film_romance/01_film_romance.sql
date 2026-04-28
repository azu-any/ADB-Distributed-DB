CREATE SCHEMA IF NOT EXISTS film_romance;
SET search_path TO film_romance;

CREATE TABLE film_romance (
  id_film INT PRIMARY KEY,
  title TEXT NOT NULL,
  duration INTERVAL,
  release_date DATE,
  classification TEXT NOT NULL DEFAULT 'Romance',
  language TEXT,
  CHECK (classification = 'Romance')
);

CREATE TABLE cast_crew_romance (
  id_person INT NOT NULL,
  id_film INT NOT NULL REFERENCES film_romance(id_film) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('Actor','Director')),
  PRIMARY KEY (id_person, id_film, role)
);

-- Partial replicas used for global search and resilience.
CREATE TABLE film_index_replica (
  id_film INT PRIMARY KEY,
  title TEXT NOT NULL,
  classification TEXT NOT NULL
);
CREATE TABLE person_basic_replica (
  id_person INT PRIMARY KEY,
  name TEXT NOT NULL,
  role TEXT NOT NULL,
  origin_region TEXT NOT NULL
);
CREATE TABLE soundtrack_index_replica (
  id_soundtrack INT PRIMARY KEY,
  title TEXT NOT NULL,
  classification TEXT NOT NULL,
  id_film INT
);

CREATE INDEX ON film_romance (classification, title);
CREATE INDEX ON cast_crew_romance (id_film, role);
