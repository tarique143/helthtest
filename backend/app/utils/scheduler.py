# backend/app/utils/scheduler.py

from sqlalchemy import and_
from datetime import datetime, time, date, timezone
from app.db.database import SessionLocal
from app.db import models
from .email_utils import send_email

def send_daily_reminders():
    """
    The main job that runs daily. It finds users with reminders for today
    and sends them a single summary email.
    """
    print(f"--- Running daily reminder job at {datetime.now()} ---")
    db = SessionLocal()
    try:
        # Get all active users
        users = db.query(models.User).filter(models.User.is_active == True).all()
        
        for user in users:
            today_start = datetime.combine(date.today(), time.min)
            
            # Find medications due today for this user
            meds_due = db.query(models.Medication).filter(
                and_(
                    models.Medication.owner_id == user.id,
                    models.Medication.frequency == "Daily",
                    # Check if last_taken_at is NULL or was before today
                    (models.Medication.last_taken_at == None) | (models.Medication.last_taken_at < today_start)
                )
            ).all()

            # Find appointments for today for this user
            today_end = datetime.combine(date.today(), time.max)
            appts_today = db.query(models.Appointment).filter(
                and_(
                    models.Appointment.owner_id == user.id,
                    models.Appointment.appointment_datetime >= today_start,
                    models.Appointment.appointment_datetime <= today_end
                )
            ).all()

            # If there's nothing to remind, skip to the next user
            if not meds_due and not appts_today:
                continue

            # --- Format the Email Content ---
            subject = "Your Daily Health Reminders"
            html_content = f"<html><body><h2>Hello {user.full_name},</h2><p>Here are your health reminders for today, {date.today().strftime('%B %d, %Y')}:</p>"
            text_content = f"Hello {user.full_name},\nHere are your reminders for today:\n"

            if meds_due:
                html_content += "<h3>💊 Medications to Take:</h3><ul>"
                text_content += "\n--- Medications to Take ---\n"
                for med in meds_due:
                    timing = med.meal_timing or (med.specific_time.strftime('%I:%M %p') if med.specific_time else '')
                    html_content += f"<li><b>{med.name}</b> ({med.dosage}) - Take {timing}</li>"
                    text_content += f"- {med.name} ({med.dosage}) - Take {timing}\n"
                html_content += "</ul>"

            if appts_today:
                html_content += "<h3>🗓️ Appointments Today:</h3><ul>"
                text_content += "\n--- Appointments Today ---\n"
                for appt in appts_today:
                    appt_time = appt.appointment_datetime.strftime('%I:%M %p')
                    html_content += f"<li><b>Dr. {appt.doctor_name}</b> at {appt_time}</li>"
                    text_content += f"- Dr. {appt.doctor_name} at {appt_time}\n"
                html_content += "</ul>"
            
            html_content += "<p>Have a healthy day!</p></body></html>"
            
            # Send the email
            send_email(user.email, subject, html_content, text_content)

    finally:
        db.close()
    print("--- Daily reminder job finished ---")