CREATE SCHEMA IF NOT EXISTS soundtrack_classical;
SET search_path TO soundtrack_classical;

CREATE TABLE soundtrack_classical (
  id_soundtrack INT PRIMARY KEY,
  title TEXT NOT NULL,
  duration INTERVAL,
  release_date DATE,
  classification TEXT NOT NULL DEFAULT 'Classical',
  language TEXT,
  id_film INT,
  CHECK (classification = 'Classical')
);

CREATE TABLE soundtrack_authorship_classical (
  id_person INT NOT NULL,
  id_soundtrack INT NOT NULL REFERENCES soundtrack_classical(id_soundtrack) ON DELETE CASCADE,
  PRIMARY KEY (id_person, id_soundtrack)
);

CREATE TABLE soundtrack_performance_classical (
  id_person INT NOT NULL,
  id_soundtrack INT NOT NULL REFERENCES soundtrack_classical(id_soundtrack) ON DELETE CASCADE,
  PRIMARY KEY (id_person, id_soundtrack)
);

-- Partial replicas used for global search and resilience.
CREATE TABLE soundtrack_index_replica (
  id_soundtrack INT PRIMARY KEY,
  title TEXT NOT NULL,
  classification TEXT NOT NULL,
  id_film INT
);
CREATE TABLE person_basic_replica (
  id_person INT PRIMARY KEY,
  name TEXT NOT NULL,
  role TEXT NOT NULL,
  origin_region TEXT NOT NULL
);
CREATE TABLE film_index_replica (
  id_film INT PRIMARY KEY,
  title TEXT NOT NULL,
  classification TEXT NOT NULL
);

CREATE INDEX ON soundtrack_classical (classification, title);
