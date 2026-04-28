CREATE SCHEMA IF NOT EXISTS regional_mx;
SET search_path TO regional_mx;

CREATE TABLE cinephile_personal_mx (
  id_cinephile INT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  phone TEXT,
  city TEXT NOT NULL,
  country_code CHAR(2) NOT NULL DEFAULT 'MX',
  CHECK (country_code = 'MX')
);

CREATE TABLE person_basic_replica (
  id_person INT PRIMARY KEY,
  name TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('Actor','Director','Producer','Author','Interpreter')),
  origin_region TEXT NOT NULL
);

CREATE TABLE person_extended_mx (
  id_person INT PRIMARY KEY,
  birth_date DATE,
  origin_region TEXT NOT NULL DEFAULT 'MX',
  CHECK (origin_region = 'MX')
);

CREATE TABLE producer_core_mx (
  id_person INT PRIMARY KEY,
  address TEXT NOT NULL,
  telephone TEXT,
  origin_region TEXT NOT NULL DEFAULT 'MX',
  CHECK (origin_region = 'MX')
);

CREATE TABLE author_interpreter_mx (
  id_person INT PRIMARY KEY,
  primary_language TEXT NOT NULL DEFAULT 'Spanish',
  origin_region TEXT NOT NULL DEFAULT 'MX',
  CHECK (primary_language IN ('Spanish'))
);

CREATE TABLE soundtrack_full_spanish (
  id_soundtrack INT PRIMARY KEY,
  title TEXT NOT NULL,
  duration INTERVAL,
  release_date DATE,
  classification TEXT NOT NULL,
  language TEXT NOT NULL DEFAULT 'Spanish',
  id_film INT,
  CHECK (language = 'Spanish')
);

CREATE INDEX ON cinephile_personal_mx (city);
CREATE INDEX ON person_basic_replica (role, name);
