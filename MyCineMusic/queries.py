from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass(frozen=True)
class QuerySpec:
    key: str
    title: str
    category: str
    description: str
    sql: str
    params: List[Dict[str, Any]]


QUERY_SPACE = [
    QuerySpec(
        key="film_by_classification",
        title="Search films by classification",
        category="Film fragments",
        description="Queries the reconstructed global.film view, which UNIONs Film_Action, Film_Romance, and Film_SciFi fragments.",
        sql="""
            SELECT id_film, title, duration, release_date, classification, language
            FROM global.film
            WHERE (%(classification)s = 'All' OR classification = %(classification)s)
              AND (%(language)s = 'All' OR language = %(language)s)
              AND (%(title_contains)s = '' OR title ILIKE '%%' || %(title_contains)s || '%%')
            ORDER BY classification, title
            LIMIT %(limit)s;
        """,
        params=[
            {"name": "classification", "label": "Classification", "type": "select", "options": ["All", "Action", "Romance", "Science Fiction"], "default": "All"},
            {"name": "language", "label": "Language", "type": "select", "options": ["All", "Spanish", "English"], "default": "All"},
            {"name": "title_contains", "label": "Title contains", "type": "text", "default": ""},
            {"name": "limit", "label": "Max rows", "type": "number", "default": 50, "min": 1, "max": 500},
        ],
    ),
    QuerySpec(
        key="film_index",
        title="Search replicated film index",
        category="Replicated indexes",
        description="Uses analytics-hosted lightweight film_index_replica for fast global search without scanning full film fragments.",
        sql="""
            SELECT id_film, title, classification
            FROM global.film_index_replica_f
            WHERE (%(classification)s = 'All' OR classification = %(classification)s)
              AND (%(title_contains)s = '' OR title ILIKE '%%' || %(title_contains)s || '%%')
            ORDER BY title
            LIMIT %(limit)s;
        """,
        params=[
            {"name": "classification", "label": "Classification", "type": "select", "options": ["All", "Action", "Romance", "Science Fiction"], "default": "All"},
            {"name": "title_contains", "label": "Title contains", "type": "text", "default": ""},
            {"name": "limit", "label": "Max rows", "type": "number", "default": 50, "min": 1, "max": 500},
        ],
    ),
    QuerySpec(
        key="cast_by_film",
        title="Cast and crew for a film",
        category="Derived film fragments",
        description="Joins cast_crew derived fragments with film and person_basic to show people associated with one film.",
        sql="""
            SELECT f.id_film, f.title AS film, f.classification, cc.role AS credit_role,
                   p.id_person, p.name AS person, p.role AS person_role, p.origin_region
            FROM global.cast_crew cc
            JOIN global.film f ON f.id_film = cc.id_film
            LEFT JOIN global.person_basic p ON p.id_person = cc.id_person
            WHERE (%(film_id)s = 0 OR f.id_film = %(film_id)s)
              AND (%(film_title)s = '' OR f.title ILIKE '%%' || %(film_title)s || '%%')
              AND (%(credit_role)s = 'All' OR cc.role = %(credit_role)s)
            ORDER BY f.title, cc.role, p.name
            LIMIT %(limit)s;
        """,
        params=[
            {"name": "film_id", "label": "Film ID (0 = ignore)", "type": "number", "default": 0, "min": 0, "max": 1000000},
            {"name": "film_title", "label": "Film title contains", "type": "text", "default": ""},
            {"name": "credit_role", "label": "Credit role", "type": "select", "options": ["All", "Director", "Actor"], "default": "All"},
            {"name": "limit", "label": "Max rows", "type": "number", "default": 100, "min": 1, "max": 500},
        ],
    ),
    QuerySpec(
        key="people_by_region_role",
        title="People by role and region",
        category="Person fragments",
        description="Queries the reconstructed person view from horizontally and vertically fragmented person data.",
        sql="""
            SELECT id_person, name, birth_date, role, origin_region
            FROM global.person
            WHERE (%(role)s = 'All' OR role = %(role)s)
              AND (%(origin_region)s = 'All' OR origin_region = %(origin_region)s)
              AND (%(name_contains)s = '' OR name ILIKE '%%' || %(name_contains)s || '%%')
            ORDER BY origin_region, role, name
            LIMIT %(limit)s;
        """,
        params=[
            {"name": "role", "label": "Role", "type": "select", "options": ["All", "Actor", "Director", "Producer", "Author", "Interpreter"], "default": "All"},
            {"name": "origin_region", "label": "Origin region", "type": "select", "options": ["All", "MX", "US"], "default": "All"},
            {"name": "name_contains", "label": "Name contains", "type": "text", "default": ""},
            {"name": "limit", "label": "Max rows", "type": "number", "default": 100, "min": 1, "max": 500},
        ],
    ),
    QuerySpec(
        key="producer_investments",
        title="Secure producer investments",
        category="Secure administrative data",
        description="Reads the restricted production_investment foreign table and joins producer/film metadata for authorized financial analysis.",
        sql="""
            SELECT pr.id_person, pb.name AS producer, f.id_film, f.title AS film,
                   pi.invested_amount, pi.currency, f.classification
            FROM global.production_investment_f pi
            JOIN global.producer pr ON pr.id_person = pi.id_person
            LEFT JOIN global.person_basic pb ON pb.id_person = pi.id_person
            LEFT JOIN global.film f ON f.id_film = pi.id_film
            WHERE (%(min_amount)s = 0 OR pi.invested_amount >= %(min_amount)s)
              AND (%(currency)s = 'All' OR pi.currency = %(currency)s)
              AND (%(producer_name)s = '' OR pb.name ILIKE '%%' || %(producer_name)s || '%%')
            ORDER BY pi.invested_amount DESC
            LIMIT %(limit)s;
        """,
        params=[
            {"name": "min_amount", "label": "Minimum amount", "type": "number", "default": 0, "min": 0, "max": 1000000000},
            {"name": "currency", "label": "Currency", "type": "select", "options": ["All", "MXN", "USD"], "default": "All"},
            {"name": "producer_name", "label": "Producer name contains", "type": "text", "default": ""},
            {"name": "limit", "label": "Max rows", "type": "number", "default": 50, "min": 1, "max": 500},
        ],
    ),
    QuerySpec(
        key="soundtrack_by_classification",
        title="Search soundtracks by classification",
        category="Soundtrack fragments",
        description="Queries the reconstructed soundtrack view from Classical, Jazz, and Pop horizontal fragments.",
        sql="""
            SELECT s.id_soundtrack, s.title, s.duration, s.release_date, s.classification,
                   s.language, s.id_film, f.title AS film
            FROM global.soundtrack s
            LEFT JOIN global.film f ON f.id_film = s.id_film
            WHERE (%(classification)s = 'All' OR s.classification = %(classification)s)
              AND (%(language)s = 'All' OR s.language = %(language)s)
              AND (%(title_contains)s = '' OR s.title ILIKE '%%' || %(title_contains)s || '%%')
            ORDER BY s.classification, s.title
            LIMIT %(limit)s;
        """,
        params=[
            {"name": "classification", "label": "Classification", "type": "select", "options": ["All", "Classical", "Jazz", "Pop"], "default": "All"},
            {"name": "language", "label": "Language", "type": "select", "options": ["All", "Spanish", "English"], "default": "All"},
            {"name": "title_contains", "label": "Title contains", "type": "text", "default": ""},
            {"name": "limit", "label": "Max rows", "type": "number", "default": 50, "min": 1, "max": 500},
        ],
    ),
    QuerySpec(
        key="soundtrack_discography",
        title="Authors and interpreters by soundtrack",
        category="Derived soundtrack fragments",
        description="Reads derived authorship and performance fragments co-located with soundtrack genre fragments.",
        sql="""
            WITH credits AS (
              SELECT id_person, id_soundtrack, 'Author' AS credit_type FROM global.soundtrack_authorship
              UNION ALL
              SELECT id_person, id_soundtrack, 'Interpreter' AS credit_type FROM global.soundtrack_performance
            )
            SELECT s.id_soundtrack, s.title AS soundtrack, s.classification, c.credit_type,
                   p.id_person, p.name, p.origin_region
            FROM credits c
            JOIN global.soundtrack s ON s.id_soundtrack = c.id_soundtrack
            LEFT JOIN global.person_basic p ON p.id_person = c.id_person
            WHERE (%(classification)s = 'All' OR s.classification = %(classification)s)
              AND (%(credit_type)s = 'All' OR c.credit_type = %(credit_type)s)
              AND (%(soundtrack_title)s = '' OR s.title ILIKE '%%' || %(soundtrack_title)s || '%%')
            ORDER BY s.title, c.credit_type, p.name
            LIMIT %(limit)s;
        """,
        params=[
            {"name": "classification", "label": "Soundtrack classification", "type": "select", "options": ["All", "Classical", "Jazz", "Pop"], "default": "All"},
            {"name": "credit_type", "label": "Credit type", "type": "select", "options": ["All", "Author", "Interpreter"], "default": "All"},
            {"name": "soundtrack_title", "label": "Soundtrack title contains", "type": "text", "default": ""},
            {"name": "limit", "label": "Max rows", "type": "number", "default": 100, "min": 1, "max": 500},
        ],
    ),
    QuerySpec(
        key="cinephile_preferences",
        title="Cinephile favorites with personal region",
        category="Analytics and personal data",
        description="Combines analytics preference tables with isolated regional personal fragments for an authorized full profile query.",
        sql="""
            SELECT cp.id_cinephile, cp.name, cp.email, cp.city, cp.country_code,
                   'Film' AS favorite_type, f.id_film AS favorite_id, f.title AS favorite_title, f.classification
            FROM global.cinephile_personal cp
            JOIN global.cinephile_fav_film_f cff ON cff.id_cinephile = cp.id_cinephile
            JOIN global.film f ON f.id_film = cff.id_film
            WHERE (%(country_code)s = 'All' OR cp.country_code = %(country_code)s)
              AND (%(cinephile_name)s = '' OR cp.name ILIKE '%%' || %(cinephile_name)s || '%%')
            UNION ALL
            SELECT cp.id_cinephile, cp.name, cp.email, cp.city, cp.country_code,
                   'Soundtrack' AS favorite_type, s.id_soundtrack AS favorite_id, s.title AS favorite_title, s.classification
            FROM global.cinephile_personal cp
            JOIN global.cinephile_fav_soundtrack_f cfs ON cfs.id_cinephile = cp.id_cinephile
            JOIN global.soundtrack s ON s.id_soundtrack = cfs.id_soundtrack
            WHERE (%(country_code)s = 'All' OR cp.country_code = %(country_code)s)
              AND (%(cinephile_name)s = '' OR cp.name ILIKE '%%' || %(cinephile_name)s || '%%')
            ORDER BY name, favorite_type, favorite_title
            LIMIT %(limit)s;
        """,
        params=[
            {"name": "country_code", "label": "Country code", "type": "select", "options": ["All", "MX", "US"], "default": "All"},
            {"name": "cinephile_name", "label": "Cinephile name contains", "type": "text", "default": ""},
            {"name": "limit", "label": "Max rows", "type": "number", "default": 100, "min": 1, "max": 500},
        ],
    ),
    QuerySpec(
        key="global_search",
        title="Global title/name search",
        category="Cross-fragment search",
        description="Searches film titles, soundtrack titles, and person names through reconstructed global views and indexes.",
        sql="""
            SELECT 'Film' AS entity_type, id_film::text AS entity_id, title AS label, classification AS detail
            FROM global.film
            WHERE title ILIKE '%%' || %(term)s || '%%'
            UNION ALL
            SELECT 'Soundtrack' AS entity_type, id_soundtrack::text AS entity_id, title AS label, classification AS detail
            FROM global.soundtrack
            WHERE title ILIKE '%%' || %(term)s || '%%'
            UNION ALL
            SELECT 'Person' AS entity_type, id_person::text AS entity_id, name AS label, role || ' / ' || origin_region AS detail
            FROM global.person_basic
            WHERE name ILIKE '%%' || %(term)s || '%%'
            ORDER BY entity_type, label
            LIMIT %(limit)s;
        """,
        params=[
            {"name": "term", "label": "Search term", "type": "text", "default": ""},
            {"name": "limit", "label": "Max rows", "type": "number", "default": 100, "min": 1, "max": 500},
        ],
    ),
]

QUERY_BY_KEY = {q.key: q for q in QUERY_SPACE}
