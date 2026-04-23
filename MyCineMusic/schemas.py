from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from decimal import Decimal

# Film Schemas
class FilmBase(BaseModel):
    title: str
    duration: Optional[int] = None
    release_date: Optional[date] = None
    classification: Optional[str] = None

class FilmCreate(FilmBase):
    pass

class Film(FilmBase):
    id_film: int
    class Config:
        from_attributes = True

# Soundtrack Schemas
class SoundtrackBase(BaseModel):
    title: str
    duration: Optional[int] = None
    release_date: Optional[date] = None
    classification: Optional[str] = None

class SoundtrackCreate(SoundtrackBase):
    pass

class Soundtrack(SoundtrackBase):
    id_soundtrack: int
    class Config:
        from_attributes = True

# Cinephile Schemas
class CinephileBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None

class CinephileCreate(CinephileBase):
    pass

class Cinephile(CinephileBase):
    id_cinephile: int
    class Config:
        from_attributes = True

class CinephilePreferences(BaseModel):
    id_cinephile: int
    fav_films: List[int] = []
    fav_soundtracks: List[int] = []

class CinephileFullProfile(BaseModel):
    profile: Cinephile
    preferences: CinephilePreferences

# Person & Producer
class PersonBase(BaseModel):
    name: str
    birth_date: Optional[date] = None
    role: Optional[str] = None
    region: Optional[str] = None

class PersonCreate(PersonBase):
    pass

class Person(PersonBase):
    id_person: int
    class Config:
        from_attributes = True

class ProducerCreate(BaseModel):
    id_person: int
    address: Optional[str] = None
    telephone: Optional[str] = None

class ProductionInvestmentCreate(BaseModel):
    id_person: int
    id_film: int
    invested_amount: Decimal
