from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
import pytz  # Import pytz for timezone handling

from app.api import deps
from app.db import models
from app.crud import crud_medication
from app.schemas import medication as medication_schema

router = APIRouter()

@router.get("/", response_model=List[medication_schema.Medication])
def read_medications(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Retrieve all medications for the current logged-in user.
    """
    medications = crud_medication.get_medications_by_user(db, owner_id=current_user.id)
    return medications


@router.post("/", response_model=medication_schema.Medication, status_code=status.HTTP_201_CREATED)
def create_medication(
    *,
    db: Session = Depends(deps.get_db),
    medication_in: medication_schema.MedicationCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Create a new medication for the current logged-in user with the new structure.
    """
    # Basic validation for timing
    if medication_in.timing_type == "Specific-Time" and not medication_in.specific_time:
        raise HTTPException(status_code=400, detail="Specific time is required for this timing type.")
    if medication_in.timing_type == "Meal-Related" and not medication_in.meal_timing:
        raise HTTPException(status_code=400, detail="Meal timing is required for this timing type.")
        
    medication = crud_medication.create_user_medication(
        db=db, medication=medication_in, owner_id=current_user.id
    )
    return medication


@router.put("/{med_id}", response_model=medication_schema.Medication)
def update_medication(
    *,
    db: Session = Depends(deps.get_db),
    med_id: int,
    medication_in: medication_schema.MedicationUpdate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Update a medication for the current user.
    """
    db_medication = crud_medication.get_medication_by_id(db, medication_id=med_id)
    if not db_medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    if db_medication.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    medication = crud_medication.update_medication(db, db_medication=db_medication, medication_in=medication_in)
    return medication


@router.delete("/{med_id}", response_model=medication_schema.Medication)
def delete_medication(
    *,
    db: Session = Depends(deps.get_db),
    med_id: int,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Delete a medication for the current user.
    """
    db_medication = crud_medication.get_medication_by_id(db, medication_id=med_id)
    if not db_medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    if db_medication.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    medication = crud_medication.delete_medication(db, db_medication=db_medication)
    return medication


@router.post("/{med_id}/taken", response_model=medication_schema.Medication)
def mark_medication_as_taken(
    *,
    db: Session = Depends(deps.get_db),
    med_id: int,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Mark a medication as taken for the current user.
    NOTE: The logic to prevent duplicate 'taken' marks on the same day has been removed
    to allow for multi-dose medications until a proper logging system is implemented.
    """
    db_medication = crud_medication.get_medication_by_id(db, medication_id=med_id)
    if not db_medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    if db_medication.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # --- LOGIC TO PREVENT DUPLICATE ENTRIES REMOVED ---
    # The check that was here previously prevented marking a medication
    # as taken more than once per day. This has been removed to support
    # medications that need to be taken multiple times a day.
    
    # Update the last_taken_at field with the current UTC time
    update_data = medication_schema.MedicationUpdate(last_taken_at=datetime.now(timezone.utc))
    medication = crud_medication.update_medication(db, db_medication=db_medication, medication_in=update_data)
    return medication

