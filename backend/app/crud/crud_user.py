# backend/app/crud/crud_user.py

from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.db import models
from app.schemas import user as user_schema
from app.core.security import get_password_hash

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Retrieves a user from the database by their ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Retrieves a user from the database by their email address."""
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: user_schema.UserCreate) -> models.User:
    """Creates a new user in the database."""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- PASTE THE NEW FUNCTION BELOW THIS LINE ---

def update_user(
    db: Session, db_user: models.User, user_in: user_schema.UserUpdate
) -> models.User:
    """
    Updates a user's profile information.
    """
    # Get the dictionary of the data to update, excluding any fields that were not sent
    update_data = user_in.model_dump(exclude_unset=True)
    
    # Set the new values on the existing user object
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.add(db_user) # Add the updated object to the session
    db.commit() # Commit the changes to the database
    db.refresh(db_user) # Refresh the object with the latest data from the DB
    return db_user
def set_password_reset_token(db: Session, db_user: models.User, token: str, expires_at: datetime) -> models.User:
    """Sets a password reset token and expiry on a user object."""
    db_user.reset_password_token = token
    db_user.reset_token_expires_at = expires_at
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user