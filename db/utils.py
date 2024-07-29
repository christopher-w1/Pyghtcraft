import hashlib
import os
import datetime
import re
from sqlalchemy.orm import Session
from sqlalchemy import exists
from .models import Authentification, WebsitePermissions, WebApiSession

def generate_salt(length=8):
    return os.urandom(length).hex()

def hash_password(password, salt):
    first_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    hasher = hashlib.sha256()
    hasher.update((first_hash + salt).encode('utf-8'))
    hashcode = hasher.hexdigest()
    return f"$SHA${salt}${hashcode}"
    
def get_user_by_username(db: Session, username: str):
    return db.query(Authentification).filter(Authentification.username == username).first()

def verify_password(stored_password: str, provided_password: str):
    if not stored_password.startswith("$SHA$"):
        return False
    salt = stored_password.split('$')[2]
    return stored_password == hash_password(provided_password, salt)

def gen_api_key(db: Session, username: str):
    api_key = "API_" + os.urandom(22).hex()
       
    # Berechtigungsstufe des Benutzers abrufen
    permission = db.query(WebsitePermissions).filter(WebsitePermissions.username == username).first()
    perm_level = 0

    if permission:
        perm_level = permission.perm_level
    
    # Berechne den Zeitpunkt, der 10 Minuten in der Zukunft liegt
    valid_until = datetime.datetime.now() + datetime.timedelta(minutes=10)
    
    # API-Schlüssel zusammen mit username, valid_until und perm_level in webapi_session abspeichern
    new_session = WebApiSession(username=username, api_key=api_key, valid_until=valid_until, perm_level=perm_level)
    db.add(new_session)
    db.commit()
    
    return api_key

def invalidate_api_key(db: Session, api_key: str):
    session = db.query(WebApiSession).filter(WebApiSession.api_key == api_key).first()
    if session:
        db.delete(session)
        db.commit()
        return "API key invalidated successfully."
    else:
        return "API key not found."
    
def is_api_key_valid(db: Session, api_key: str):
    # Überprüfen, ob der API-Schlüssel gültig ist (valid_until in der Zukunft)
    session = db.query(WebApiSession).filter(WebApiSession.api_key == api_key).first()
    return session and session.valid_until > datetime.datetime.now()
    
def is_perm_level_sufficient(db: Session, api_key: str, required_level: int):
    # Überprüfen, ob die Berechtigungsstufe des API-Schlüssels ausreichend ist
    session = db.query(WebApiSession).filter(WebApiSession.api_key == api_key).first()
    return session and session.perm_level >= required_level
    
def is_action_permitted(db: Session, username: str, api_key: str, required_level: int):
    session = db.query(WebApiSession).filter(WebApiSession.api_key == api_key).first()
    return (session and session.perm_level >= required_level and 
        session.valid_until > datetime.datetime.now() and session.username==username)