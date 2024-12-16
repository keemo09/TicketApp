from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI  # Angenommene Konfigurationsdatei

# Engine und Session erstellen
engine = create_engine(DATABASE_URI)  # remove connection args in case using POSTRESQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency, to get DB-Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()