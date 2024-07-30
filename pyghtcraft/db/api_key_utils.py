import os
import datetime
from sqlalchemy.orm import Session
from config import Config
from .models import WebsitePermissions, WebApiSession

keycounter = 0

def generate_hex(length=32):
    # Generate a random hexadecimal string of a given length
    return os.urandom((length+1)//2).hex()[:length]

def gen_api_key(db: Session, username: str):
    """
    Generates and returns a new API key for the given user.
    """
    global keycounter
    api_key = f"{keycounter:03d}_{generate_hex(28)}"
       
    # Get user's permission level from the database
    permission = db.query(WebsitePermissions).filter(WebsitePermissions.username == username).first()
    
    if permission:
        perm_level = permission.perm_level
    else:
        # Set level to 0 if no entry
        perm_level = 0
    
    # Calculate validity duration
    valid_until = datetime.datetime.now() + datetime.timedelta(minutes=Config.KEY_VALID_DURATION)
    
    # Save API key with username, valid_until and perm_level in webapi_session
    new_session = WebApiSession(username=username, api_key=api_key, valid_until=valid_until, perm_level=perm_level)
    db.add(new_session)
    db.commit()
    return api_key

def invalidate_api_key(db: Session, api_key: str):
    """
    Invalidates the given API key.
    """
    session = db.query(WebApiSession).filter(WebApiSession.api_key == api_key).first()
    if session:
        db.delete(session)
        db.commit()
        return "API key invalidated successfully."
    else:
        return "API key not found."
    
def delete_expired_api_keys_for_user(db: Session, username: str):
    # Delete expired API keys for a specific user
    now = datetime.datetime.now()
    
    expired_sessions = db.query(WebApiSession).filter(WebApiSession.username == username, WebApiSession.valid_until < now).all()
    
    for session in expired_sessions:
        db.delete(session)
    db.commit()

def is_api_key_valid(db: Session, api_key: str):
    """
    Checks if an API key is still valid.
    """
    session = db.query(WebApiSession).filter(WebApiSession.api_key == api_key).first()
    return session and session.valid_until > datetime.datetime.now()
    
def is_perm_level_sufficient(db: Session, api_key: str, required_level: int):
    """
    Checks if the API key owner's permission level is at least the required level.
    """
    session = db.query(WebApiSession).filter(WebApiSession.api_key == api_key).first()
    return session and session.perm_level >= required_level
    
def is_action_permitted(db: Session, username: str, api_key: str, required_level: int):
    """
    Checks if the API key owner is permitted to perform an action.
    Unlike is_perm_level_sufficient, it also checks if the key is used by the rightful
    owner, which is safer.
    """
    session = db.query(WebApiSession).filter(WebApiSession.api_key == api_key).first()
    return (session and session.perm_level >= required_level and 
            session.valid_until > datetime.datetime.now() and session.username == username) 
   
def get_perm_level(db: Session, username: str, api_key: str):
    """
    Returns the permission level associated with the users api key.
    Returns 0 if the key is stolen from another user.
    """
    session = db.query(WebApiSession).filter(WebApiSession.api_key == api_key).first()
    return session.perm_level if session.username == username else 0
