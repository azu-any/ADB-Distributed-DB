from sqlalchemy.orm import Session
from fastapi import HTTPException
import models
import schemas

# --- Film Services (Replicated across all nodes) ---

def create_film(db_regional: Session, db_global: Session, db_secure: Session, film: schemas.FilmCreate):
    # Create the object
    db_film = models.Film(**film.model_dump())
    
    # Needs to be replicated to all nodes
    try:
        if db_regional:
            db_regional.add(models.Film(**film.model_dump()))
        if db_global:
            db_global.add(models.Film(**film.model_dump()))
        if db_secure:
            db_secure.add(models.Film(**film.model_dump()))
        
        # In a real distributed transaction (2PC), this is much more complex.
        # Here we do a simple commit.
        if db_regional: db_regional.commit()
        if db_global: db_global.commit()
        if db_secure: db_secure.commit()
        
        # Just returning from one to show the ID
        # Note: If IDs are auto-incrementing independently, they might drift.
        # A true DDBMS usually relies on UUIDs or a global sequence generator.
        if db_global:
            db_global.refresh(db_film)
        return db_film
    except Exception as e:
        if db_regional: db_regional.rollback()
        if db_global: db_global.rollback()
        if db_secure: db_secure.rollback()
        raise HTTPException(status_code=500, detail=f"Replication failed: {str(e)}")

def get_films(db: Session, skip: int = 0, limit: int = 100):
    # Can read from any node because it's replicated. We pass one session here (e.g., global)
    return db.query(models.Film).offset(skip).limit(limit).all()


# --- Cinephile Services (Vertically Fragmented) ---

def create_cinephile(db_regional: Session, db_global: Session, cinephile: schemas.CinephileCreate):
    # Sensitive data goes to Regional
    # We will simulate the same ID by inserting to Regional first and getting the ID
    try:
        # 1. Insert into Regional Node (Sensitive Data)
        db_cin_regional = models.Cinephile(
            name=cinephile.name,
            email=cinephile.email,
            phone=cinephile.phone,
            city=cinephile.city
        )
        db_regional.add(db_cin_regional)
        db_regional.commit()
        db_regional.refresh(db_cin_regional)
        
        # 2. Insert into Global Node (ID only, for preferences later)
        db_cin_global = models.Cinephile(id_cinephile=db_cin_regional.id_cinephile)
        db_global.add(db_cin_global)
        db_global.commit()
        
        return db_cin_regional
    except Exception as e:
        db_regional.rollback()
        db_global.rollback()
        raise HTTPException(status_code=500, detail=f"Fragmentation insert failed: {str(e)}")

def get_cinephile_full_profile(db_regional: Session, db_global: Session, cinephile_id: int):
    # 1. Fetch sensitive info from Regional
    cin_regional = db_regional.query(models.Cinephile).filter(models.Cinephile.id_cinephile == cinephile_id).first()
    if not cin_regional:
        raise HTTPException(status_code=404, detail="Cinephile not found")
        
    # 2. Fetch preferences from Global
    fav_films = db_global.query(models.CinephileFavFilm).filter(models.CinephileFavFilm.id_cinephile == cinephile_id).all()
    fav_soundtracks = db_global.query(models.CinephileFavSoundtrack).filter(models.CinephileFavSoundtrack.id_cinephile == cinephile_id).all()
    
    # 3. Application-level Join
    preferences = schemas.CinephilePreferences(
        id_cinephile=cinephile_id,
        fav_films=[f.id_film for f in fav_films],
        fav_soundtracks=[s.id_soundtrack for s in fav_soundtracks]
    )
    
    return schemas.CinephileFullProfile(
        profile=cin_regional,
        preferences=preferences
    )


# --- Producer / Financial Services (Strictly Secure Node) ---

def create_production_investment(db_secure: Session, investment: schemas.ProductionInvestmentCreate):
    db_investment = models.ProductionInvestment(**investment.model_dump())
    try:
        db_secure.add(db_investment)
        db_secure.commit()
        db_secure.refresh(db_investment)
        return db_investment
    except Exception as e:
        db_secure.rollback()
        raise HTTPException(status_code=500, detail=f"Secure node insert failed: {str(e)}")
