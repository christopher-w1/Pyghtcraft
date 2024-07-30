import os, datetime, logging, hashlib, base64
from sqlalchemy.orm import Session
from config import Config
from .models import WebsitePermissions, WebApiSession


logger = logging.getLogger()
keycounter = 1

def generate_hex(length=16):
    """
    Generates a random hexadecimal string.
    """
    return os.urandom((length+1)//2).hex()[:length]

def gen_base64_salt(input_str: str, number: int, length=16):
    """
    Generates a salt by base64-encoding a string with a number.
    """
    hash_object = hashlib.sha256((f'{number}{input_str}').encode())
    hash_bytes = hash_object.digest()
    base64_encoded = base64.urlsafe_b64encode(hash_bytes).decode()
    return base64_encoded[:length]

def gen_api_key(db: Session, username: str):
    """
    Generates and returns a new API key for the given user.
    """
    global keycounter
    api_key = f"{gen_base64_salt(username, keycounter, 8)}{generate_hex(24)}"
    keycounter += 1
       
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
    delete_expired_api_keys_for_user(db, username)
    logger.info(f"Generated new API key for {username}, Permission Level {perm_level}, valid until {valid_until}.")
    return api_key, perm_level

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
    if expired_sessions:
        for session in expired_sessions:
            db.delete(session)
    db.commit()

def is_api_key_valid_old(db: Session, api_key: str):
    """
    Checks if an API key is still valid.
    """
    session = db.query(WebApiSession).filter(WebApiSession.api_key == api_key).first()
    if session is None: return False
    return session and session.valid_until > datetime.datetime.now()
    
def is_api_key_valid(db: Session, username: str, api_key: str):
    """
    Checks if an API key is still valid.
    """
    session = db.query(WebApiSession).filter(WebApiSession.username == username, WebApiSession.api_key == api_key).first()
    if session is None: return False
    return session and session.valid_until > datetime.datetime.now()

def is_action_permitted_old(db: Session, username: str, api_key: str, required_level: int):
    """
    Checks if the API key owner is permitted to perform an action.
    Unlike is_perm_level_sufficient, it also checks if the key is used by the rightful
    owner, which is safer.
    """
    session = db.query(WebApiSession).filter(WebApiSession.api_key == api_key).first()
    if session is None: return False
    return (session and session.perm_level >= required_level and 
            session.valid_until > datetime.datetime.now() and session.username == username) 
    
def is_action_permitted(db: Session, username: str, api_key: str, required_level: int):
    """
    Checks if the API key owner is permitted to perform an action.
    Unlike is_perm_level_sufficient, it also checks if the key is used by the rightful
    owner, which is safer.
    """
    session = db.query(WebApiSession).filter(WebApiSession.username == username, WebApiSession.api_key == api_key).first()
    if session is None: return False
    return (session.perm_level >= required_level and session.valid_until > datetime.datetime.now() and session.username == username) 
   
def get_perm_level(db: Session, api_key: str, username: str) -> int:
    """
    Returns permission level of a user identified by api-key and username.
    
    Args:
        db (Session): Database session.
        username (str): User name.
        api_key (str): API key.
        
    Returns:
        int: Permission level. Returns 0 if not found.
    """
    session = db.query(WebApiSession).filter(WebApiSession.username == username, WebApiSession.api_key == api_key).first()
    if session:
        return session.perm_level
    return 0

