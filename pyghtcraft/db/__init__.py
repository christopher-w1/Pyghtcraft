from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import logging
#from ..config import Config

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisiere die Engine
DATABASE_URL = "mysql+pymysql://myuser:mypassword@localhost/mydatabase"
engine = create_engine(DATABASE_URL)

# Erstelle eine SessionLocal für die Datenbankverbindung
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definiere die Basis-Klasse für die Modelle
Base = declarative_base()

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    try:
        # Alle Tabellen basierend auf den Modellen erstellen
        Base.metadata.create_all(bind=engine)
        logger.info("Tabellen erfolgreich erstellt.")
    except Exception as e:
        logger.error(f"Fehler beim Erstellen der Tabellen: {e}")

if __name__ == "__main__":
    print("Creating tables...")
    create_tables()
