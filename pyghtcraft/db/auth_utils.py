import hashlib
import os
import datetime
import re
from sqlalchemy.orm import Session
from sqlalchemy import exists
from .models import Authentification, WebsitePermissions

def get_user_by_username(db: Session, username: str):
    return db.query(Authentification).filter(Authentification.username == username).first()

def generate_random_hex(length=16):
    # Generate a random hexadecimal string of a given length
    return os.urandom((length+1)//2).hex()[:length]

def hash_password(password, salt):
    # Hash the password with a given salt using SHA-256
    first_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    hasher = hashlib.sha256()
    hasher.update((first_hash + salt).encode('utf-8'))
    hashcode = hasher.hexdigest()
    return f"$SHA${salt}${hashcode}"

def current_millis():
    # Return the current time in milliseconds
    return int(datetime.datetime.now().timestamp() * 1000)

def is_valid_email(email):
    """
    Check if an email address has a valid format.

    :param email: The email address to check.
    :return: True if the email address is valid, otherwise False.
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def check_and_insert_user(db: Session, username: str, clear_password: str, email: str, ip: str):
    # Check if user already exists
    user_exists = db.query(exists().where(Authentification.username == username)).scalar()

    if len(clear_password) < 7:
        return "Error: Password must be at least 7 characters!"
    
    if len(username) < 3:
        return "Error: Name must be at least 3 characters!"
    
    if not is_valid_email(email):
        return f"Error: {email} is not a valid E-Mail address!"

    if not user_exists:
        # Hash the password
        salt = generate_random_hex()
        hashed_password = hash_password(clear_password, salt)
        # Create auth database column model
        new_user = Authentification(username=username.lower(), 
                                    password=hashed_password, 
                                    realname=username, 
                                    email=email, 
                                    regip=ip,
                                    regdate=current_millis())
        db.add(new_user)
        # Check if user already has a permission entry and keep it
        permission = db.query(WebsitePermissions).filter(WebsitePermissions.username == username).first()
        if not permission:
            new_permission = WebsitePermissions(username=username.lower(), perm_level=1)
            db.add(new_permission)
        db.commit()
        return "User registered successfully!"
    else:
        return "A user with this name already exists!"

def verify_password(stored_password: str, provided_password: str):
    # Verify the provided password against the stored hashed password
    if not stored_password.startswith("$SHA$"):
        return False
    salt = stored_password.split('$')[2]
    return stored_password == hash_password(provided_password, salt)
