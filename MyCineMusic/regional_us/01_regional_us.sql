CREATE SCHEMA IF NOT EXISTS regional_us;
SET search_path TO regional_us;

CREATE TABLE cinephile_personal_us (
  id_cinephile INT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  phone TEXT,
  city TEXT NOT NULL,
  country_code CHAR(2) NOT NULL DEFAULT 'US',
  CHECK (country_code = 'US')
);

CREATE TABLE person_basic_replica (
  id_person INT PRIMARY KEY,
  name TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('Actor','Director','Producer','Author','Interpreter')),
  origin_region TEXT NOT NULL
);

CREATE TABLE person_extended_us (
  id_person INT PRIMARY KEY,
  birth_date DATE,
  origin_region TEXT NOT NULL DEFAULT 'US',
  CHECK (origin_region = 'US')
);

CREATE TABLE producer_core_us (
  id_person INT PRIMARY KEY,
  address TEXT NOT NULL,
  telephone TEXT,
  origin_region TEXT NOT NULL DEFAULT 'US',
  CHECK (origin_region = 'US')
);

CREATE TABLE author_interpreter_us (
  id_person INT PRIMARY KEY,
  primary_language TEXT NOT NULL DEFAULT 'English',
  origin_region TEXT NOT NULL DEFAULT 'US',
  CHECK (primary_language IN ('English'))
);

CREATE TABLE soundtrack_full_english (
  id_soundtrack INT PRIMARY KEY,
  title TEXT NOT NULL,
  duration INTERVAL,
  release_date DATE,
  classification TEXT NOT NULL,
  language TEXT NOT NULL DEFAULT 'English',
  id_film INT,
  CHECK (language = 'English')
);

CREATE INDEX ON cinephile_personal_us (city);
CREATE INDEX ON person_basic_replica (role, name);
