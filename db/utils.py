
import datetime, os
from sqlalchemy.orm import Session
from config import Config
from .models import Authentification, WebsitePermissions, WebApiSession

keycounter = 0

def generate_hex(length=32):
    return os.urandom((length+1)/2).hex()[length:]
    
def get_user_by_username(db: Session, username: str):
    return db.query(Authentification).filter(Authentification.username == username).first()

def gen_api_key(db: Session, username: str):
    """
        Generates and return a new API key for the given user.
    """
    api_key = f"{keycounter:03d}_{generate_hex(28)}"
       
    # Get users permission level from database
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
    
def is_api_key_valid(db: Session, api_key: str):
    """
        Checks if API key is still valid.
    """
    session = db.query(WebApiSession).filter(WebApiSession.api_key == api_key).first()
    return session and session.valid_until > datetime.datetime.now()
    
def is_perm_level_sufficient(db: Session, api_key: str, required_level: int):
    """
        Checks if API key owners permission level is at least the required level.
    """
    session = db.query(WebApiSession).filter(WebApiSession.api_key == api_key).first()
    return session and session.perm_level >= required_level
    
def is_action_permitted(db: Session, username: str, api_key: str, required_level: int):
    """
        Checks if API key owner is permitted to perform an action.
        Unlike is_perm_level_sufficient it also checks if key is used by the rightful
        owner which is safer.
    """
    session = db.query(WebApiSession).filter(WebApiSession.api_key == api_key).first()
    return (session and session.perm_level >= required_level and 
        session.valid_until > datetime.datetime.now() and session.username==username)