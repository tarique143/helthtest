# backend/app/schemas/medication.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import time, datetime

# --- Base Schema ---
class MedicationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    dosage: str = Field(..., min_length=1, max_length=100)
    
    timing_type: str # "Meal-Related" or "Specific-Time"
    meal_timing: Optional[str] = None # "After Breakfast", etc.
    specific_time: Optional[time] = None # 09:00:00
    
    frequency: str # "Daily", "As Needed"


# --- Schema for Creating a Medication ---
class MedicationCreate(MedicationBase):
    pass


# --- Schema for Updating a Medication ---
# All fields are optional
class MedicationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    dosage: Optional[str] = Field(None, min_length=1, max_length=100)
    
    timing_type: Optional[str] = None
    meal_timing: Optional[str] = None
    specific_time: Optional[time] = None
    
    frequency: Optional[str] = None


# --- Schema for Reading/Returning a Medication ---
class Medication(MedicationBase):
    id: int
    owner_id: int
    last_taken_at: Optional[datetime] = None # Include tracking field

    class Config:
        from_attributes = True

# --- Schema for Marking as Taken ---
class MedicationMarkAsTaken(BaseModel):
    taken_at: datetime