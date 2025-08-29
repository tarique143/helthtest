# backend/app/api/v1/endpoints/dashboard.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from datetime import datetime, time, date, timezone

from app.api import deps
from app.db import models

router = APIRouter()

@router.get("/")
def get_dashboard_data(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Retrieve real, personalized dashboard data for the current user.
    """
    # 1. Get today's medications
    # This finds medications that are 'Daily' and were not taken today,
    # OR medications with a specific time for today.
    today = date.today()
    meds_today_query = (
        db.query(models.Medication)
        .filter(models.Medication.owner_id == current_user.id)
        .filter(
            and_(
                models.Medication.frequency == "Daily",
                # Check if last_taken_at is NULL or was before today
                (models.Medication.last_taken_at == None) | (models.Medication.last_taken_at < datetime.combine(today, time.min))
            )
        )
    )
    meds_today = meds_today_query.all()
    
    # Convert to a list of simple dicts for the frontend
    medications_for_dashboard = [
        {"name": med.name, "dosage": med.dosage, "timing": med.meal_timing or med.specific_time.strftime('%I:%M %p')}
        for med in meds_today
    ]

    # 2. Get the next upcoming appointment
    next_appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.owner_id == current_user.id)
        .filter(models.Appointment.appointment_datetime >= datetime.now(timezone.utc))
        .order_by(models.Appointment.appointment_datetime)
        .first()
    )
    
    # 3. Get a random health tip (for now, it's static)
    # In a real app, you would have a health_tips table and query a random one.
    health_tip = "Stay hydrated by drinking plenty of water throughout the day."
    
    return {
        "user_full_name": current_user.full_name,
        "medications_today": medications_for_dashboard,
        "next_appointment": next_appointment, # Will be None if no upcoming appointments
        "health_tip": health_tip
    }