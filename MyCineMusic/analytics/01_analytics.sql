CREATE SCHEMA IF NOT EXISTS analytics;
SET search_path TO analytics;

CREATE TABLE cinephile_key (
  id_cinephile INT PRIMARY KEY,
  home_region TEXT NOT NULL CHECK (home_region IN ('MX','US','OTHER'))
);

CREATE TABLE cinephile_fav_film (
  id_cinephile INT NOT NULL REFERENCES cinephile_key(id_cinephile) ON DELETE CASCADE,
  id_film INT NOT NULL,
  PRIMARY KEY (id_cinephile, id_film)
);

CREATE TABLE cinephile_fav_soundtrack (
  id_cinephile INT NOT NULL REFERENCES cinephile_key(id_cinephile) ON DELETE CASCADE,
  id_soundtrack INT NOT NULL,
  PRIMARY KEY (id_cinephile, id_soundtrack)
);

CREATE TABLE film_index_replica (
  id_film INT PRIMARY KEY,
  title TEXT NOT NULL,
  classification TEXT NOT NULL
);
CREATE TABLE soundtrack_index_replica (
  id_soundtrack INT PRIMARY KEY,
  title TEXT NOT NULL,
  classification TEXT NOT NULL,
  id_film INT
);
CREATE INDEX ON cinephile_fav_film (id_film);
CREATE INDEX ON cinephile_fav_soundtrack (id_soundtrack);
