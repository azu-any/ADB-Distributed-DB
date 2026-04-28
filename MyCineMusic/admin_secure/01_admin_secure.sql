CREATE SCHEMA IF NOT EXISTS admin_secure;
SET search_path TO admin_secure;

CREATE TABLE production_investment (
  id_person INT NOT NULL,
  id_film INT NOT NULL,
  invested_amount NUMERIC(14,2) NOT NULL CHECK (invested_amount >= 0),
  currency CHAR(3) NOT NULL DEFAULT 'USD',
  PRIMARY KEY (id_person, id_film)
);

CREATE TABLE producer_name_replica (
  id_person INT PRIMARY KEY,
  name TEXT NOT NULL,
  origin_region TEXT NOT NULL
);
REVOKE ALL ON SCHEMA admin_secure FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA admin_secure FROM PUBLIC;
