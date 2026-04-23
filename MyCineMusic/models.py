from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base

# Note: In a true DDBMS, not all columns exist on every physical node table.
# For SQLAlchemy ORM, we define the full logical schema, and use specific columns 
# during querying depending on which node we are connected to.

class Film(Base):
    __tablename__ = "film"
    id_film = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    duration = Column(Integer)
    release_date = Column(Date)
    classification = Column(String(50)) # e.g., Action, Romance

class Soundtrack(Base):
    __tablename__ = "soundtrack"
    id_soundtrack = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    duration = Column(Integer)
    release_date = Column(Date)
    classification = Column(String(50))

class Cinephile(Base):
    __tablename__ = "cinephile"
    # Vertically Fragmented:
    # Node 1 (Regional) stores: id_cinephile, name, email, phone, city
    # Node 2 (Global) stores: id_cinephile and the associative relationships
    id_cinephile = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    city = Column(String(100))

class Person(Base):
    __tablename__ = "person"
    id_person = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    birth_date = Column(Date)
    role = Column(String(50)) # Actor, Director, Author, Interpreter
    region = Column(String(50)) # For horizontal fragmentation

class Producer(Base):
    __tablename__ = "producer"
    id_person = Column(Integer, ForeignKey("person.id_person"), primary_key=True)
    address = Column(String(255))
    telephone = Column(String(50))

# Associative Entities
class CastCrew(Base):
    __tablename__ = "cast_crew"
    id_person = Column(Integer, ForeignKey("person.id_person"), primary_key=True)
    id_film = Column(Integer, ForeignKey("film.id_film"), primary_key=True)
    role = Column(String(100))

class ProductionInvestment(Base):
    __tablename__ = "production_investment"
    id_person = Column(Integer, ForeignKey("person.id_person"), primary_key=True)
    id_film = Column(Integer, ForeignKey("film.id_film"), primary_key=True)
    invested_amount = Column(Numeric(15, 2))

class SoundtrackAuthorship(Base):
    __tablename__ = "soundtrack_authorship"
    id_person = Column(Integer, ForeignKey("person.id_person"), primary_key=True)
    id_soundtrack = Column(Integer, ForeignKey("soundtrack.id_soundtrack"), primary_key=True)

class SoundtrackPerformance(Base):
    __tablename__ = "soundtrack_performance"
    id_person = Column(Integer, ForeignKey("person.id_person"), primary_key=True)
    id_soundtrack = Column(Integer, ForeignKey("soundtrack.id_soundtrack"), primary_key=True)

class CinephileFavFilm(Base):
    __tablename__ = "cinephile_fav_film"
    id_cinephile = Column(Integer, ForeignKey("cinephile.id_cinephile"), primary_key=True)
    id_film = Column(Integer, ForeignKey("film.id_film"), primary_key=True)

class CinephileFavSoundtrack(Base):
    __tablename__ = "cinephile_fav_soundtrack"
    id_cinephile = Column(Integer, ForeignKey("cinephile.id_cinephile"), primary_key=True)
    id_soundtrack = Column(Integer, ForeignKey("soundtrack.id_soundtrack"), primary_key=True)
