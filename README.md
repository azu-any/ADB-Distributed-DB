# MyCineMusic Distributed Database Management System

Welcome to the backend repository for **MyCineMusic**, a Distributed Database Management System built for a university project. This backend is designed to connect to three separate PostgreSQL nodes hosted on DigitalOcean, implementing custom fragmentation and replication strategies at the application layer.

## Architecture
 **1 coordinador** (puerto 5432): expone vistas globales `global.*` mediante `postgres_fdw`.
- **2 nodos regionales** (`regional_mx`, `regional_us`): datos de personas y cinephiles según ubicación geográfica.
- **3 fragmentos de películas** (`film_action`, `film_romance`, `film_scifi`): fragmentación horizontal por clasificación.
- **3 fragmentos de soundtracks** (`soundtrack_classical`, `soundtrack_jazz`, `soundtrack_pop`): fragmentación horizontal por género musical.
- **1 nodo de analítica** (`analytics`): claves de cinephiles y relaciones no sensibles (favoritos).
- **1 nodo administrativo seguro** (`admin_secure`): datos financieros de inversiones no replicados.

**Tech Stack**: Python, Streamlit.

---

## Setup Instructions for Teammates

Follow these steps to get the project running locally:

### 1. Prerequisites
- Python 3.9+ installed on your machine.
- Access to the 3 DigitalOcean PostgreSQL connection strings.

### 2. Installation
Navigate into the backend directory:
```bash
cd MyCineMusic
```

*(Optional but recommended)* Create and activate a virtual environment:
```bash
python3 -m venv venv
Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Variables Configuration
In the `MyCineMusic` directory, you will find a `.env` file with placeholder connection strings. You **must** update this file with the actual DigitalOcean credentials provided by the team lead:

```ini
NODE_REGIONAL_URL=postgresql://user:password@regional-node-host:5432/mycinemusic
NODE_GLOBAL_URL=postgresql://user:password@global-node-host:5432/mycinemusic
NODE_SECURE_URL=postgresql://user:password@secure-node-host:5432/mycinemusic
```

### 4. Running the Server
Start the FastAPI development server using `uvicorn`:
```bash
uvicorn main:app --reload
```
The server will start at `http://127.0.0.1:8000`.

### 5. API Documentation
Once the server is running, navigate to the automatically generated Swagger UI documentation to test the distributed endpoints:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## How It Works (The Routing Layer)

Because this is a DDBMS, standard ORM CRUD operations are not enough. All database operations must pass through our custom Service/Routing layer located in `services.py`.

- **Replicated Data (e.g., Films)**: The application explicitly opens sessions to all 3 nodes and commits the data everywhere to ensure high availability.
- **Vertically Fragmented Data (e.g., Cinephile Profiles)**: The application splits incoming JSON payloads. Sensitive data is saved to `engine_regional`, while the ID is saved to `engine_global`.
- **Application-Level Joins**: When retrieving a full `Cinephile` profile, the application queries Node 1 for sensitive info, Node 2 for preferences, and merges them into a single Pydantic response model.
