# backend/app/schemas/user.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

# --- Base Schemas ---
# These contain the common fields shared across other schemas.

class UserBase(BaseModel):
    """Base schema for user, contains shared attributes."""
    email: EmailStr
    full_name: Optional[str] = None
    dob: Optional[date] = None
    address: Optional[str] = None

# --- Schemas for Specific Operations ---

# Schema for creating a new user (e.g., in a POST request)
# This schema expects a password.
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


# Schema for updating a user's profile
# All fields are optional, so the user can update only what they need.
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    dob: Optional[date] = None
    address: Optional[str] = None


# Schema for reading/returning user data (e.g., in a GET response)
# This schema should NEVER include the password.
class User(UserBase):
    id: int
    is_active: bool

    class Config:
        # This tells Pydantic to read the data even if it is not a dict,
        # but an ORM model (or any other arbitrary object with attributes).
        from_attributes = True