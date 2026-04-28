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