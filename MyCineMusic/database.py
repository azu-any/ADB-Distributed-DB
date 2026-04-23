import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Get connection URLs from environment variables
NODE_REGIONAL_URL = os.getenv("NODE_REGIONAL_URL")
NODE_GLOBAL_URL = os.getenv("NODE_GLOBAL_URL")
NODE_SECURE_URL = os.getenv("NODE_SECURE_URL")

# Create Engines
# Echo is set to True to see the generated SQL for educational/debugging purposes
engine_regional = create_engine(NODE_REGIONAL_URL, echo=True) if NODE_REGIONAL_URL else None
engine_global = create_engine(NODE_GLOBAL_URL, echo=True) if NODE_GLOBAL_URL else None
engine_secure = create_engine(NODE_SECURE_URL, echo=True) if NODE_SECURE_URL else None

# Create SessionLocal class for each node
SessionLocalRegional = sessionmaker(autocommit=False, autoflush=False, bind=engine_regional) if engine_regional else None
SessionLocalGlobal = sessionmaker(autocommit=False, autoflush=False, bind=engine_global) if engine_global else None
SessionLocalSecure = sessionmaker(autocommit=False, autoflush=False, bind=engine_secure) if engine_secure else None

Base = declarative_base()

# Dependency wrappers for FastAPI
def get_db_regional():
    if not SessionLocalRegional:
        raise Exception("Regional node connection not configured.")
    db = SessionLocalRegional()
    try:
        yield db
    finally:
        db.close()

def get_db_global():
    if not SessionLocalGlobal:
        raise Exception("Global node connection not configured.")
    db = SessionLocalGlobal()
    try:
        yield db
    finally:
        db.close()

def get_db_secure():
    if not SessionLocalSecure:
        raise Exception("Secure node connection not configured.")
    db = SessionLocalSecure()
    try:
        yield db
    finally:
        db.close()
