import os
from contextlib import contextmanager
from typing import Any, Dict, Iterable, Optional

import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DEFAULTS = {
    "host": os.getenv("PGHOST", "localhost"),
    "port": int(os.getenv("PGPORT", "5432")),
    "dbname": os.getenv("PGDATABASE", "mycinemusic"),
    "user": os.getenv("PGUSER", "postgres"),
    "password": os.getenv("PGPASSWORD", "postgres"),
}


def get_conn_params(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    params = DEFAULTS.copy()
    if overrides:
        params.update({k: v for k, v in overrides.items() if v not in (None, "")})
    return params


@contextmanager
def connect(overrides: Optional[Dict[str, Any]] = None):
    conn = psycopg2.connect(**get_conn_params(overrides))
    try:
        yield conn
    finally:
        conn.close()


def run_query(sql: str, params: Optional[Dict[str, Any]] = None, overrides: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    with connect(overrides) as conn:
        return pd.read_sql_query(sql, conn, params=params or {})


def test_connection(overrides: Optional[Dict[str, Any]] = None) -> str:
    df = run_query("SELECT current_database() AS database, current_user AS user, version() AS version", overrides=overrides)
    row = df.iloc[0]
    return f"Connected to {row['database']} as {row['user']}"
