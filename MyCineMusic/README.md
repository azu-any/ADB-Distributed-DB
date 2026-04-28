# MyCineMusic Streamlit Query Interface

This Streamlit app connects your Python project to the Docker-based distributed PostgreSQL database through the **coordinator** node on `localhost:5432`.

## Architecture

```text
Streamlit app / Python project
        |
        | psycopg2, parameterized SQL
        v
PostgreSQL coordinator: localhost:5432 / mycinemusic / schema global
        |
        | postgres_fdw foreign tables and global views
        v
Regional, genre, analytics, and secure admin PostgreSQL nodes
```

The app queries the `global` schema exposed by the coordinator. It does not connect directly to every fragment node; the coordinator already reconstructs the global relations with `UNION ALL` views and foreign tables.

## Query space included

| Option | Query | Main schema objects |
|---:|---|---|
| 1 | Search films by classification | `global.film` |
| 2 | Search replicated film index | `global.film_index_replica_f` |
| 3 | Cast and crew for a film | `global.cast_crew`, `global.film`, `global.person_basic` |
| 4 | People by role and region | `global.person` |
| 5 | Secure producer investments | `global.production_investment_f`, `global.producer`, `global.film` |
| 6 | Search soundtracks by classification | `global.soundtrack`, `global.film` |
| 7 | Authors and interpreters by soundtrack | `global.soundtrack_authorship`, `global.soundtrack_performance`, `global.soundtrack` |
| 8 | Cinephile favorites with personal region | `global.cinephile_personal`, analytics favorites, `global.film`, `global.soundtrack` |
| 9 | Global title/name search | `global.film`, `global.soundtrack`, `global.person_basic` |

All user inputs are passed as query parameters, not string-concatenated into SQL.

## Run

```bash
# Start the distributed DB first, from the SQL package directory
cd mycinemusic_distributed_db
docker compose up -d

# Start the Python interface
cd ../mycinemusic_streamlit_app
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Default connection:

```env
PGHOST=localhost
PGPORT=5432
PGDATABASE=mycinemusic
PGUSER=postgres
PGPASSWORD=postgres
PGSCHEMA=global
```

## Files

- `app.py` - Streamlit UI, menu, parameters, results table, CSV export.
- `db.py` - PostgreSQL connection and query execution helpers.
- `queries.py` - Query catalog/query space.
- `requirements.txt` - Python dependencies.
- `.env.example` - Example connection settings.
# MyCineMusic Distributed DBMS

Proyecto final de Bases de Datos Avanzadas – LIS 3012.
Despliegue de una base de datos distribuida basada en PostgreSQL utilizando Docker y `postgres_fdw`.
El diseño sigue un modelo de fragmentación horizontal, vertical y derivada, con réplicas parciales y nodos especializados para cumplir con los requerimientos del mini-mundo MyCineMusic.

## Arquitectura

- **1 coordinador** (puerto 5432): expone vistas globales `global.*` mediante `postgres_fdw`.
- **2 nodos regionales** (`regional_mx`, `regional_us`): datos de personas y cinephiles según ubicación geográfica.
- **3 fragmentos de películas** (`film_action`, `film_romance`, `film_scifi`): fragmentación horizontal por clasificación.
- **3 fragmentos de soundtracks** (`soundtrack_classical`, `soundtrack_jazz`, `soundtrack_pop`): fragmentación horizontal por género musical.
- **1 nodo de analítica** (`analytics`): claves de cinephiles y relaciones no sensibles (favoritos).
- **1 nodo administrativo seguro** (`admin_secure`): datos financieros de inversiones no replicados.

Todos los contenedores son PostgreSQL 16 y se comunican a través de una red interna `mycine_net`.

## Requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac/Linux)
- Cliente `psql` (opcional; se puede usar el del contenedor del coordinador)

## Instrucciones para ejecutar

1. Clonar este repositorio:
   ```bash
   git clone <URL-del-repo>
   cd MyCineMusic
