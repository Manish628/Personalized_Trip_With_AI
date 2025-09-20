from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///trips.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String)
    dates = Column(String)
    interests = Column(String)
    budget = Column(String)
    itinerary = Column(Text)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_trip(destination, dates, interests, budget, itinerary):
    db = SessionLocal()
    new_trip = Trip(destination=destination, dates=dates, interests=interests, budget=budget, itinerary=itinerary)
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    db.close()
    return new_trip

def get_all_trips():
    db = SessionLocal()
    trips = db.query(Trip).all()
    db.close()
    return [{"destination": t.destination, "dates": t.dates, "interests": t.interests, "budget": t.budget, "itinerary": t.itinerary} for t in trips]