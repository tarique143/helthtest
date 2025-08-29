# backend/app/db/models.py

from sqlalchemy import (
    Boolean, Column, Integer, String, DateTime, Date, ForeignKey, Text, Time
)
from sqlalchemy.orm import relationship
import datetime

# Import the Base class from our database setup
from .database import Base

class User(Base):
    """
    User model for the 'users' table.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Optional profile details
    dob = Column(Date) # Date of Birth
    address = Column(String)
     # --- NEW COLUMNS FOR PASSWORD RESET ---
    reset_password_token = Column(String, unique=True, nullable=True)
    reset_token_expires_at = Column(DateTime, nullable=True)
    
    # Relationships: A single user can have multiple items of the following
    medications = relationship("Medication", back_populates="owner")
    appointments = relationship("Appointment", back_populates="owner")
    contacts = relationship("EmergencyContact", back_populates="owner")

class Medication(Base):
    """
    UPDATED Medication model.
    """
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    
    # New, more structured timing fields
    timing_type = Column(String, default="Meal-Related") # "Meal-Related" or "Specific-Time"
    meal_timing = Column(String, nullable=True) # "After Breakfast", etc.
    specific_time = Column(Time, nullable=True) # 09:00:00

    # New frequency field
    frequency = Column(String, default="Daily") # "Daily", "As Needed"

    # New field for tracking
    last_taken_at = Column(DateTime, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="medications")
class Appointment(Base):
    """
    Appointment model for the 'appointments' table.
    """
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_name = Column(String, nullable=False)
    appointment_datetime = Column(DateTime, nullable=False)
    location = Column(String)
    purpose = Column(String)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationship: Connects this appointment back to the User
    owner = relationship("User", back_populates="appointments")

class EmergencyContact(Base):
    """
    EmergencyContact model for the 'emergency_contacts' table.
    """
    __tablename__ = "emergency_contacts"

    id = Column(Integer, primary_key=True, index=True)
    contact_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    relationship_type = Column(String) # e.g., "Son", "Doctor", "Neighbor"
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationship: Connects this contact back to the User
    owner = relationship("User", back_populates="contacts")

class HealthTip(Base):
    """
    HealthTip model for the 'health_tips' table.
    This table is not tied to a specific user.
    """
    __tablename__ = "health_tips"
    
    id = Column(Integer, primary_key=True, index=True)
    tip_text = Column(Text, nullable=False)
    category = Column(String, default="General") # e.g., "Diet", "Exercise"