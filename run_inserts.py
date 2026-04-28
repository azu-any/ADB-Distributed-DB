import re
from typing import Dict

import psycopg2

# Mapping of schema names to their external ports
SCHEMA_TO_PORT = {
    "regional_mx": 5433,
    "regional_us": 5434,
    "film_action": 5435,
    "film_romance": 5436,
    "film_scifi": 5437,
    "soundtrack_classical": 5438,
    "soundtrack_jazz": 5439,
    "soundtrack_pop": 5440,
    "analytics": 5441,
    "admin_secure": 5442,
}


def run_inserts():
    with open("MyCineMusic/insert_samples.sql", "r") as f:
        content = f.read()

    # Split by semicolon but keep the semicolon
    statements = content.split(";")

    for stmt in statements:
        stmt = stmt.strip()
        if not stmt or not stmt.startswith("INSERT INTO"):
            continue

        # Extract schema name: INSERT INTO schema_name.table_name
        match = re.search(r"INSERT INTO\s+([\w_]+)\.", stmt, re.IGNORECASE)
        if match:
            schema = match.group(1).lower()
            if schema in SCHEMA_TO_PORT:
                port = SCHEMA_TO_PORT[schema]
                print(f"Executing on port {port} (schema {schema})...")
                try:
                    conn = psycopg2.connect(
                        host="localhost",
                        port=port,
                        user="postgres",
                        password="postgres",
                        dbname="mycinemusic",
                    )
                    conn.autocommit = True
                    with conn.cursor() as cur:
                        cur.execute(stmt)
                    conn.close()
                except Exception as e:
                    print(f"Error on {schema} (port {port}): {e}")
            else:
                print(f"Unknown schema: {schema}")


if __name__ == "__main__":
    run_inserts()
