from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import services
from database import engine_regional, engine_global, engine_secure, get_db_regional, get_db_global, get_db_secure

# In a real environment, you might only create tables on the specific nodes they belong to.
# For simplicity in this DDBMS simulation, if engines exist we create the logical schema.
# In production, alembic migrations would target specific databases.
if engine_regional: models.Base.metadata.create_all(bind=engine_regional)
if engine_global: models.Base.metadata.create_all(bind=engine_global)
if engine_secure: models.Base.metadata.create_all(bind=engine_secure)

app = FastAPI(title="MyCineMusic DDBMS API", description="Distributed Database Management System Backend")

@app.get("/")
def read_root():
    return {"message": "Welcome to MyCineMusic DDBMS API. The system is distributed across 3 nodes."}

# --- Replicated Data Endpoints ---

@app.post("/films/", response_model=schemas.Film)
def create_film(
    film: schemas.FilmCreate, 
    db_regional: Session = Depends(get_db_regional),
    db_global: Session = Depends(get_db_global),
    db_secure: Session = Depends(get_db_secure)
):
    """
    Creates a film. Because this is core catalog data, it is REPLICATED across all 3 nodes.
    """
    return services.create_film(db_regional, db_global, db_secure, film)

@app.get("/films/", response_model=List[schemas.Film])
def read_films(skip: int = 0, limit: int = 100, db_global: Session = Depends(get_db_global)):
    """
    Reads films. Because data is replicated, we can query any single node (e.g., Global).
    """
    return services.get_films(db_global, skip=skip, limit=limit)

# --- Vertically Fragmented Endpoints ---

@app.post("/cinephiles/", response_model=schemas.Cinephile)
def create_cinephile(
    cinephile: schemas.CinephileCreate,
    db_regional: Session = Depends(get_db_regional),
    db_global: Session = Depends(get_db_global)
):
    """
    Creates a cinephile profile. Uses VERTICAL FRAGMENTATION.
    Sensitive data (Name, Email, etc.) -> Regional Node.
    ID (for preferences) -> Global Node.
    """
    return services.create_cinephile(db_regional, db_global, cinephile)

@app.get("/cinephiles/{cinephile_id}", response_model=schemas.CinephileFullProfile)
def get_cinephile(
    cinephile_id: int,
    db_regional: Session = Depends(get_db_regional),
    db_global: Session = Depends(get_db_global)
):
    """
    Fetches a full cinephile profile by performing an Application-Level Join
    between the Regional Node (sensitive data) and the Global Node (preferences).
    """
    return services.get_cinephile_full_profile(db_regional, db_global, cinephile_id)

# --- Secure Node Endpoints ---

@app.post("/investments/", response_model=schemas.ProductionInvestmentCreate)
def create_investment(
    investment: schemas.ProductionInvestmentCreate,
    db_secure: Session = Depends(get_db_secure)
):
    """
    Creates a financial record. Strictly stored ONLY on the Secure Node.
    """
    return services.create_production_investment(db_secure, investment)
