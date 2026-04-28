CREATE EXTENSION IF NOT EXISTS postgres_fdw;
CREATE SCHEMA IF NOT EXISTS global;
SET search_path TO global;

-- Foreign servers. Docker Compose service names are used as host names.
CREATE SERVER regional_mx_srv FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'regional_mx', dbname 'mycinemusic', port '5432');
CREATE SERVER regional_us_srv FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'regional_us', dbname 'mycinemusic', port '5432');
CREATE SERVER film_action_srv FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'film_action', dbname 'mycinemusic', port '5432');
CREATE SERVER film_romance_srv FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'film_romance', dbname 'mycinemusic', port '5432');
CREATE SERVER film_scifi_srv FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'film_scifi', dbname 'mycinemusic', port '5432');
CREATE SERVER soundtrack_classical_srv FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'soundtrack_classical', dbname 'mycinemusic', port '5432');
CREATE SERVER soundtrack_jazz_srv FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'soundtrack_jazz', dbname 'mycinemusic', port '5432');
CREATE SERVER soundtrack_pop_srv FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'soundtrack_pop', dbname 'mycinemusic', port '5432');
CREATE SERVER analytics_srv FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'analytics', dbname 'mycinemusic', port '5432');
CREATE SERVER admin_secure_srv FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'admin_secure', dbname 'mycinemusic', port '5432');

DO $$
DECLARE s TEXT;
BEGIN
  FOREACH s IN ARRAY ARRAY['regional_mx_srv','regional_us_srv','film_action_srv','film_romance_srv','film_scifi_srv','soundtrack_classical_srv','soundtrack_jazz_srv','soundtrack_pop_srv','analytics_srv','admin_secure_srv'] LOOP
    EXECUTE format('CREATE USER MAPPING IF NOT EXISTS FOR postgres SERVER %I OPTIONS (user %L, password %L)', s, 'postgres', 'postgres');
  END LOOP;
END $$;

-- Film horizontal fragments by classification.
CREATE FOREIGN TABLE film_action_f (id_film INT, title TEXT, duration INTERVAL, release_date DATE, classification TEXT, language TEXT)
  SERVER film_action_srv OPTIONS (schema_name 'film_action', table_name 'film_action');
CREATE FOREIGN TABLE film_romance_f (id_film INT, title TEXT, duration INTERVAL, release_date DATE, classification TEXT, language TEXT)
  SERVER film_romance_srv OPTIONS (schema_name 'film_romance', table_name 'film_romance');
CREATE FOREIGN TABLE film_scifi_f (id_film INT, title TEXT, duration INTERVAL, release_date DATE, classification TEXT, language TEXT)
  SERVER film_scifi_srv OPTIONS (schema_name 'film_scifi', table_name 'film_scifi');
CREATE VIEW film AS
  SELECT * FROM film_action_f
  UNION ALL SELECT * FROM film_romance_f
  UNION ALL SELECT * FROM film_scifi_f;

-- Cinephile vertical fragments: personal regional data is isolated; preference data lives on analytics.
CREATE FOREIGN TABLE cinephile_personal_mx_f (id_cinephile INT, name TEXT, email TEXT, phone TEXT, city TEXT, country_code CHAR(2))
  SERVER regional_mx_srv OPTIONS (schema_name 'regional_mx', table_name 'cinephile_personal_mx');
CREATE FOREIGN TABLE cinephile_personal_us_f (id_cinephile INT, name TEXT, email TEXT, phone TEXT, city TEXT, country_code CHAR(2))
  SERVER regional_us_srv OPTIONS (schema_name 'regional_us', table_name 'cinephile_personal_us');
CREATE FOREIGN TABLE cinephile_key_f (id_cinephile INT, home_region TEXT)
  SERVER analytics_srv OPTIONS (schema_name 'analytics', table_name 'cinephile_key');
CREATE FOREIGN TABLE cinephile_fav_film_f (id_cinephile INT, id_film INT)
  SERVER analytics_srv OPTIONS (schema_name 'analytics', table_name 'cinephile_fav_film');
CREATE FOREIGN TABLE cinephile_fav_soundtrack_f (id_cinephile INT, id_soundtrack INT)
  SERVER analytics_srv OPTIONS (schema_name 'analytics', table_name 'cinephile_fav_soundtrack');
CREATE VIEW cinephile_personal AS
  SELECT * FROM cinephile_personal_mx_f
  UNION ALL SELECT * FROM cinephile_personal_us_f;

-- Person horizontal by region plus vertical split of basic vs extended attributes.
CREATE FOREIGN TABLE person_basic_mx_f (id_person INT, name TEXT, role TEXT, origin_region TEXT)
  SERVER regional_mx_srv OPTIONS (schema_name 'regional_mx', table_name 'person_basic_replica');
CREATE FOREIGN TABLE person_basic_us_f (id_person INT, name TEXT, role TEXT, origin_region TEXT)
  SERVER regional_us_srv OPTIONS (schema_name 'regional_us', table_name 'person_basic_replica');
CREATE FOREIGN TABLE person_extended_mx_f (id_person INT, birth_date DATE, origin_region TEXT)
  SERVER regional_mx_srv OPTIONS (schema_name 'regional_mx', table_name 'person_extended_mx');
CREATE FOREIGN TABLE person_extended_us_f (id_person INT, birth_date DATE, origin_region TEXT)
  SERVER regional_us_srv OPTIONS (schema_name 'regional_us', table_name 'person_extended_us');
CREATE VIEW person_basic AS
  SELECT * FROM person_basic_mx_f
  UNION ALL SELECT * FROM person_basic_us_f;
CREATE VIEW person_extended AS
  SELECT * FROM person_extended_mx_f
  UNION ALL SELECT * FROM person_extended_us_f;
CREATE VIEW person AS
  SELECT b.id_person, b.name, e.birth_date, b.role, b.origin_region
  FROM person_basic b LEFT JOIN person_extended e USING (id_person, origin_region);

-- Producer core data by region; sensitive investments remain on restricted admin server.
CREATE FOREIGN TABLE producer_core_mx_f (id_person INT, address TEXT, telephone TEXT, origin_region TEXT)
  SERVER regional_mx_srv OPTIONS (schema_name 'regional_mx', table_name 'producer_core_mx');
CREATE FOREIGN TABLE producer_core_us_f (id_person INT, address TEXT, telephone TEXT, origin_region TEXT)
  SERVER regional_us_srv OPTIONS (schema_name 'regional_us', table_name 'producer_core_us');
CREATE FOREIGN TABLE production_investment_f (id_person INT, id_film INT, invested_amount NUMERIC(14,2), currency CHAR(3))
  SERVER admin_secure_srv OPTIONS (schema_name 'admin_secure', table_name 'production_investment');
CREATE VIEW producer AS
  SELECT * FROM producer_core_mx_f
  UNION ALL SELECT * FROM producer_core_us_f;

-- Cast/Crew derived horizontal fragments co-located with film fragments.
CREATE FOREIGN TABLE cast_crew_action_f (id_person INT, id_film INT, role TEXT)
  SERVER film_action_srv OPTIONS (schema_name 'film_action', table_name 'cast_crew_action');
CREATE FOREIGN TABLE cast_crew_romance_f (id_person INT, id_film INT, role TEXT)
  SERVER film_romance_srv OPTIONS (schema_name 'film_romance', table_name 'cast_crew_romance');
CREATE FOREIGN TABLE cast_crew_scifi_f (id_person INT, id_film INT, role TEXT)
  SERVER film_scifi_srv OPTIONS (schema_name 'film_scifi', table_name 'cast_crew_scifi');
CREATE VIEW cast_crew AS
  SELECT * FROM cast_crew_action_f
  UNION ALL SELECT * FROM cast_crew_romance_f
  UNION ALL SELECT * FROM cast_crew_scifi_f;

-- Soundtrack horizontal fragments by classification; full language/regional copies are separate and non-replicated.
CREATE FOREIGN TABLE soundtrack_classical_f (id_soundtrack INT, title TEXT, duration INTERVAL, release_date DATE, classification TEXT, language TEXT, id_film INT)
  SERVER soundtrack_classical_srv OPTIONS (schema_name 'soundtrack_classical', table_name 'soundtrack_classical');
CREATE FOREIGN TABLE soundtrack_jazz_f (id_soundtrack INT, title TEXT, duration INTERVAL, release_date DATE, classification TEXT, language TEXT, id_film INT)
  SERVER soundtrack_jazz_srv OPTIONS (schema_name 'soundtrack_jazz', table_name 'soundtrack_jazz');
CREATE FOREIGN TABLE soundtrack_pop_f (id_soundtrack INT, title TEXT, duration INTERVAL, release_date DATE, classification TEXT, language TEXT, id_film INT)
  SERVER soundtrack_pop_srv OPTIONS (schema_name 'soundtrack_pop', table_name 'soundtrack_pop');
CREATE VIEW soundtrack AS
  SELECT * FROM soundtrack_classical_f
  UNION ALL SELECT * FROM soundtrack_jazz_f
  UNION ALL SELECT * FROM soundtrack_pop_f;

-- Discography relationships derived from soundtrack classification.
CREATE FOREIGN TABLE soundtrack_authorship_classical_f (id_person INT, id_soundtrack INT)
  SERVER soundtrack_classical_srv OPTIONS (schema_name 'soundtrack_classical', table_name 'soundtrack_authorship_classical');
CREATE FOREIGN TABLE soundtrack_authorship_jazz_f (id_person INT, id_soundtrack INT)
  SERVER soundtrack_jazz_srv OPTIONS (schema_name 'soundtrack_jazz', table_name 'soundtrack_authorship_jazz');
CREATE FOREIGN TABLE soundtrack_authorship_pop_f (id_person INT, id_soundtrack INT)
  SERVER soundtrack_pop_srv OPTIONS (schema_name 'soundtrack_pop', table_name 'soundtrack_authorship_pop');
CREATE VIEW soundtrack_authorship AS
  SELECT * FROM soundtrack_authorship_classical_f
  UNION ALL SELECT * FROM soundtrack_authorship_jazz_f
  UNION ALL SELECT * FROM soundtrack_authorship_pop_f;

CREATE FOREIGN TABLE soundtrack_performance_classical_f (id_person INT, id_soundtrack INT)
  SERVER soundtrack_classical_srv OPTIONS (schema_name 'soundtrack_classical', table_name 'soundtrack_performance_classical');
CREATE FOREIGN TABLE soundtrack_performance_jazz_f (id_person INT, id_soundtrack INT)
  SERVER soundtrack_jazz_srv OPTIONS (schema_name 'soundtrack_jazz', table_name 'soundtrack_performance_jazz');
CREATE FOREIGN TABLE soundtrack_performance_pop_f (id_person INT, id_soundtrack INT)
  SERVER soundtrack_pop_srv OPTIONS (schema_name 'soundtrack_pop', table_name 'soundtrack_performance_pop');
CREATE VIEW soundtrack_performance AS
  SELECT * FROM soundtrack_performance_classical_f
  UNION ALL SELECT * FROM soundtrack_performance_jazz_f
  UNION ALL SELECT * FROM soundtrack_performance_pop_f;

-- Lightweight replicated indexes exposed from analytics node.
CREATE FOREIGN TABLE film_index_replica_f (id_film INT, title TEXT, classification TEXT)
  SERVER analytics_srv OPTIONS (schema_name 'analytics', table_name 'film_index_replica');
CREATE FOREIGN TABLE soundtrack_index_replica_f (id_soundtrack INT, title TEXT, classification TEXT, id_film INT)
  SERVER analytics_srv OPTIONS (schema_name 'analytics', table_name 'soundtrack_index_replica');
