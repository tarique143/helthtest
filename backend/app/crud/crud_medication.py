# backend/app/crud/crud_medication.py (Updated and Corrected Version)

from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import models
from app.schemas import medication as medication_schema

def get_medication_by_id(db: Session, medication_id: int) -> Optional[models.Medication]:
    """
    Retrieves a single medication by its ID.
    """
    return db.query(models.Medication).filter(models.Medication.id == medication_id).first()

def get_medications_by_user(db: Session, owner_id: int) -> List[models.Medication]:
    """
    Retrieves all medications for a specific user.
    """
    return db.query(models.Medication).filter(models.Medication.owner_id == owner_id).all()


def create_user_medication(
    db: Session, medication: medication_schema.MedicationCreate, owner_id: int
) -> models.Medication:
    """
    Creates a new medication associated with a user.
    """
    # Use .model_dump() for modern Pydantic versions
    db_medication = models.Medication(**medication.model_dump(), owner_id=owner_id)
    db.add(db_medication)
    db.commit()
    db.refresh(db_medication)
    return db_medication


def update_medication(
    db: Session, db_medication: models.Medication, medication_in: medication_schema.MedicationUpdate
) -> models.Medication:
    """
    Updates a medication's details.
    This is the crucial function that saves the "last_taken_at" time.
    """
    # Use .model_dump() with exclude_unset=True
    update_data = medication_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_medication, key, value)
    
    db.add(db_medication)
    db.commit() # This line saves the changes to the database.
    db.refresh(db_medication)
    return db_medication


def delete_medication(db: Session, db_medication: models.Medication) -> models.Medication:
    """
    Deletes a medication from the database.
    """
    db.delete(db_medication)
    db.commit()
    return db_medication

