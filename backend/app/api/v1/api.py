# backend/app/api/v1/api.py

from fastapi import APIRouter

from app.api.v1.endpoints import (
    users, 
    auth, 
    dashboard, 
    medications,
    appointments,  # <-- IMPORT appointments
    contacts
)

# Create the main router for API version 1
api_router = APIRouter()

# Include routers
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(medications.router, prefix="/medications", tags=["Medications"])
api_router.include_router(appointments.router, prefix="/appointments", tags=["Appointments"]) # <-- ADD this line
api_router.include_router(contacts.router, prefix="/contacts", tags=["Contacts"]) # <-- ADD this line