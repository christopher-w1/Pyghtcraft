from sqlalchemy import create_engine, Column, Integer, String, Float, exists, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib, os, datetime

# Konfiguriere die Datenbankverbindung
DATABASE_URL = "mysql://authme:mccxggf@localhost/mineauth"

# Erstelle die Datenbank-Engine
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Definiere das Modell für die Tabelle 'authentifications'
class Authentification(Base):
    __tablename__ = 'authentifications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    realname = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    x = Column(Float, nullable=False, default=0.5)
    y = Column(Float, nullable=False, default=65.0)
    z = Column(Float, nullable=False, default=0.5)
    regdate = Column(BigInteger, nullable=False, default=0.5)
    regip = Column(String(40), nullable=False, default="0.0.0.0")
    email = Column(String(255), nullable=False)


def generate_salt(length=8):
    return os.urandom(length).hex()

def hash_password(password, salt):
    # Erstes SHA-256 Hash des Passworts
    first_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    # Zweites SHA-256 Hash von (erstes Hash + salt)
    hasher = hashlib.sha256()
    hasher.update((first_hash + salt).encode('utf-8'))
    hashcode = hasher.hexdigest()
    return f"$SHA${salt}${hashcode}"

def current_millis():
    return int(datetime.datetime.now().timestamp() * 1000)

def check_and_insert_user(username: str, clear_password: str, email: str, ip: str):
    # Erstelle eine Session
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # Überprüfen, ob der Benutzername bereits existiert
        user_exists = session.query(exists().where(Authentification.username == username)).scalar()

        if not user_exists:
            # Einfügen des neuen Benutzers
            salt = generate_salt()
            hashed_password = hash_password(clear_password, salt)
            new_user = Authentification(username=username.lower(), 
                                        password=hashed_password, 
                                        realname=username, 
                                        email=email, 
                                        regip=ip,
                                        regdate=current_millis())
            session.add(new_user)
            session.commit()
            return "New user registered successfully!"
        else:
            return "Name already in use."
    except Exception as e:
        session.rollback()
        return "Database error!"
    finally:
        session.close()

