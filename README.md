# MyCineMusic Distributed Database Management System

Welcome to the backend repository for **MyCineMusic**, a Distributed Database Management System built for a university project. This backend is designed to connect to three separate PostgreSQL nodes hosted on DigitalOcean, implementing custom fragmentation and replication strategies at the application layer.

## Introduction

MyCineMusic is a Distributed Database Management System (DDBMS) developed as part of a university project with the objective of applying distributed database concepts in a real-world inspired multimedia platform. The system manages information related to films, soundtracks, cinephile profiles, analytics data, and administrative records by distributing information across multiple PostgreSQL nodes instead of relying on a single centralized database.

The main goal of the project is to demonstrate how fragmentation, replication, distributed querying, and coordinated transaction management can be implemented at the application level using modern backend technologies. To achieve this, the architecture separates data according to category, region, and sensitivity, allowing the system to simulate the behavior of large-scale distributed information systems used in modern streaming and entertainment platforms.

The distributed architecture is composed of several specialized nodes, each with a specific responsibility within the system. A coordinator node exposes global views through PostgreSQL Foreign Data Wrappers (FDW), allowing the application to access distributed information transparently. Regional nodes store user and cinephile information according to geographic location, while film and soundtrack nodes implement horizontal fragmentation strategies based on genre classifications. Additionally, the project includes an analytics node dedicated to non-sensitive user relationships and recommendation data, as well as a secure administrative node that stores financial and investment-related information separately from the rest of the distributed environment.

The backend was implemented using Python together with FastAPI to expose API endpoints and coordinate communication between distributed nodes. Instead of depending exclusively on traditional ORM operations, the system implements a custom service and routing layer responsible for determining where data should be stored, replicated, or retrieved. This layer handles distributed operations such as replicated writes, fragmented inserts, and application-level joins between multiple nodes.

For replicated entities such as films, the application explicitly connects to several database nodes and propagates changes across them to improve data availability and consistency. For vertically fragmented information, such as cinephile profiles, sensitive and non-sensitive attributes are separated into different nodes according to security and organizational requirements. During retrieval operations, the backend reconstructs complete entities by querying multiple distributed databases and combining the results into unified response models.

The project also makes use of Docker and Docker Compose to simplify deployment and configuration of the distributed environment. SQL initialization scripts are used to configure schemas, fragments, global views, and node-specific data structures automatically. This approach allows the system to be reproduced consistently across development environments while reducing manual configuration effort.

Beyond its technical implementation, MyCineMusic demonstrates important software engineering and distributed systems principles, including modularity, scalability, maintainability, separation of concerns, and secure data organization. The project serves as a practical example of how distributed database concepts can be integrated into modern application architectures while addressing real-world challenges related to data distribution, synchronization, and query coordination.

## Architecture
 **1 coordinator** (port 5432): exposes global views `global.*` thorugh `postgres_fdw`.
- **2 regional nodes** (`regional_mx`, `regional_us`): data on people and cinephiles according to geographical location.
- **3 movie fragments** (`film_action`, `film_romance`, `film_scifi`): horizontal fragmentation by classification.
- **3 soundtrack fragments** (`soundtrack_classical`, `soundtrack_jazz`, `soundtrack_pop`): horizontal fragmentation by music genre.
- **1 analitics node** (`analytics`): cinephile keys and non-sensitive relationships (favorites).
- **1 secure administrative node** (`admin_secure`): unreplicated investment financial data.

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

---

## Conclusion

The MyCineMusic project successfully demonstrates the design and implementation of a distributed database management system capable of handling multimedia information across multiple specialized PostgreSQL nodes. Through the use of fragmentation, replication, distributed routing, and coordinated query processing, the system provides a practical example of how distributed database concepts can be applied in a modern application environment.

One of the most important aspects of the project is the use of horizontal and vertical fragmentation strategies to organize information according to functionality, geographic region, and data sensitivity. Film and soundtrack information is distributed across genre-specific nodes, while cinephile and administrative data are separated according to regional and security requirements. This architecture improves modularity and allows each node to focus on a specific subset of responsibilities within the system.

The implementation of PostgreSQL Foreign Data Wrappers and global views enabled the coordinator node to expose distributed information in a unified manner, simplifying access to fragmented data. At the same time, the custom routing and service layer developed in Python provided greater flexibility than traditional ORM-based approaches by explicitly managing distributed writes, replicated operations, and application-level joins between independent database nodes.

The project also highlighted the importance of software engineering practices in distributed systems development. By separating responsibilities into modules such as routing services, query handling, database configuration, and schema definitions, the system became easier to maintain, extend, and debug. The use of Docker-based deployment further improved reproducibility and simplified the setup process for development and testing environments.

From an academic perspective, the project reinforced key distributed database concepts including data fragmentation, distributed transparency, replication management, distributed querying, and node coordination. Additionally, it demonstrated how backend technologies such as FastAPI and PostgreSQL can be combined to create scalable distributed architectures capable of supporting complex information systems.

Although the system successfully fulfills its primary objectives, several future improvements could further enhance its capabilities. Potential extensions include automated replication management, distributed transaction coordination, fault tolerance mechanisms, authentication and authorization systems, query optimization strategies, and real-time monitoring tools for distributed nodes.

Overall, MyCineMusic represents a successful integration of distributed database theory and practical backend development. The project provides a scalable and modular foundation for multimedia information management while demonstrating the advantages and challenges associated with designing and implementing distributed database systems in real-world scenarios.
