-- =============================================
-- MyCineMusic - Muestra de datos distribuidos
-- Ejecutar desde el coordinador después de que
-- todos los nodos estén arriba.
-- =============================================

-- Películas en sus fragmentos por clasificación
INSERT INTO film_action.film_action (id_film, title, duration, release_date, classification, language)
VALUES (1, 'Misión Imposible: Fallout', '02:27:00', '2018-07-27', 'Action', 'English');

INSERT INTO film_romance.film_romance (id_film, title, duration, release_date, classification, language)
VALUES (2, 'The Notebook', '02:03:00', '2004-06-25', 'Romance', 'English');

INSERT INTO film_scifi.film_scifi (id_film, title, duration, release_date, classification, language)
VALUES (3, 'Interstellar', '02:49:00', '2014-11-07', 'Science Fiction', 'English');

-- Personas básicas (replicadas en cada región)
INSERT INTO regional_mx.person_basic_replica (id_person, name, role, origin_region)
VALUES 
(1, 'Guillermo del Toro', 'Director', 'MX'),
(2, 'Gael García Bernal', 'Actor', 'MX'),
(5, 'Alejandro González Iñárritu', 'Producer', 'MX');

INSERT INTO regional_us.person_basic_replica (id_person, name, role, origin_region)
VALUES 
(3, 'Christopher Nolan', 'Director', 'US'),
(4, 'Margot Robbie', 'Actor', 'US'),
(6, 'Hans Zimmer', 'Author', 'US'),
(7, 'John Williams', 'Author', 'US');

-- Datos extendidos de persona (solo en su región)
INSERT INTO regional_mx.person_extended_mx (id_person, birth_date, origin_region)
VALUES 
(1, '1964-10-09', 'MX'),
(2, '1978-11-30', 'MX'),
(5, '1963-08-15', 'MX');

INSERT INTO regional_us.person_extended_us (id_person, birth_date, origin_region)
VALUES 
(3, '1970-07-30', 'US'),
(4, '1990-07-02', 'US'),
(6, '1957-09-12', 'US'),
(7, '1932-02-08', 'US');

-- Productores
INSERT INTO regional_mx.producer_core_mx (id_person, address, telephone, origin_region)
VALUES (5, 'Av. Reforma 222, CDMX', '555-0303', 'MX');

INSERT INTO regional_us.producer_core_us (id_person, address, telephone, origin_region)
VALUES (6, '123 Hollywood Blvd, LA', '555-0404', 'US');

-- Inversiones (solo en nodo seguro)
INSERT INTO admin_secure.production_investment (id_person, id_film, invested_amount, currency)
VALUES 
(5, 1, 5000000.00, 'USD'),
(6, 3, 10000000.00, 'USD');

-- Elenco (co‑ubicado con las películas)
INSERT INTO film_action.cast_crew_action (id_person, id_film, role)
VALUES (1, 1, 'Director'), (4, 1, 'Actor');

INSERT INTO film_romance.cast_crew_romance (id_person, id_film, role)
VALUES (3, 2, 'Director'), (2, 2, 'Actor');

INSERT INTO film_scifi.cast_crew_scifi (id_person, id_film, role)
VALUES (3, 3, 'Director'), (4, 3, 'Actor');

-- Soundtracks por clasificación
INSERT INTO soundtrack_classical.soundtrack_classical (id_soundtrack, title, duration, release_date, classification, language, id_film)
VALUES (10, 'Interstellar Main Theme', '00:02:00', '2014-11-07', 'Classical', 'English', 3);

INSERT INTO soundtrack_jazz.soundtrack_jazz (id_soundtrack, title, duration, release_date, classification, language, id_film)
VALUES (11, 'La La Land Medley', '00:05:00', '2016-12-09', 'Jazz', 'English', NULL);

INSERT INTO soundtrack_pop.soundtrack_pop (id_soundtrack, title, duration, release_date, classification, language, id_film)
VALUES (12, 'A Star Is Born', '00:04:00', '2018-10-05', 'Pop', 'English', NULL);

-- Autoría e interpretación
INSERT INTO soundtrack_classical.soundtrack_authorship_classical (id_person, id_soundtrack)
VALUES (6, 10);
INSERT INTO soundtrack_classical.soundtrack_performance_classical (id_person, id_soundtrack)
VALUES (7, 10);

INSERT INTO soundtrack_jazz.soundtrack_authorship_jazz (id_person, id_soundtrack)
VALUES (7, 11);

INSERT INTO soundtrack_pop.soundtrack_authorship_pop (id_person, id_soundtrack)
VALUES (6, 12);

-- Cinephiles (personales en cada región)
INSERT INTO regional_mx.cinephile_personal_mx (id_cinephile, name, email, phone, city, country_code)
VALUES (101, 'Carlos López', 'carlos@example.mx', '555-0101', 'CDMX', 'MX');

INSERT INTO regional_us.cinephile_personal_us (id_cinephile, name, email, phone, city, country_code)
VALUES (102, 'John Smith', 'john@example.us', '555-0202', 'New York', 'US');

-- Claves y preferencias (analytics)
INSERT INTO analytics.cinephile_key (id_cinephile, home_region)
VALUES (101, 'MX'), (102, 'US');

INSERT INTO analytics.cinephile_fav_film (id_cinephile, id_film)
VALUES (101, 1), (102, 2);

INSERT INTO analytics.cinephile_fav_soundtrack (id_cinephile, id_soundtrack)
VALUES (101, 12), (102, 10);

-- Consultas de verificación (opcional, puedes correrlas después)
SELECT '--- Películas (vista global) ---' AS info;
SELECT * FROM global.film;

SELECT '--- Personas (vista global) ---' AS info;
SELECT * FROM global.person;

SELECT '--- Productores (vista global) ---' AS info;
SELECT * FROM global.producer;

SELECT '--- Inversiones (solo admin_secure) ---' AS info;
SELECT * FROM global.production_investment;

SELECT '--- Reparto completo (vista global) ---' AS info;
SELECT * FROM global.cast_crew;

SELECT '--- Soundtracks (vista global) ---' AS info;
SELECT * FROM global.soundtrack;

SELECT '--- Autoría de soundtracks (vista global) ---' AS info;
SELECT * FROM global.soundtrack_authorship;

SELECT '--- Cinephiles (vista global) ---' AS info;
SELECT * FROM global.cinephile_personal;

SELECT '--- Preferencias de cine (analytics) ---' AS info;
SELECT * FROM global.cinephile_fav_film;