# frontend/auth/service.py (FINAL, VERIFIED VERSION)

import requests
import json
from typing import List, Dict, Any

# Define the base URL of your FastAPI backend
BASE_URL = "http://127.0.0.1:8000/api/v1"
TOKEN_COOKIE_NAME = "senior_citizen_support_token"

def register_user(full_name: str, email: str, password: str) -> tuple[bool, str]:
    url = f"{BASE_URL}/users/"
    user_data = {"full_name": full_name, "email": email, "password": password}
    try:
        response = requests.post(url, json=user_data)
        if response.status_code == 201: return True, "Account created successfully! Please login."
        else: return False, f"Registration failed: {response.json().get('detail', 'Unknown error')}"
    except: return False, "Server communication error."

def login_user(email: str, password: str) -> tuple[bool, str | dict]:
    url = f"{BASE_URL}/auth/login/access-token"
    form_data = {"username": email, "password": password}
    try:
        response = requests.post(url, data=form_data)
        if response.status_code == 200: return True, response.json()
        else: return False, f"Login failed: {response.json().get('detail', 'Unknown error')}"
    except: return False, "Server communication error."

def get_dashboard_data(token: str) -> tuple[bool, dict | str]:
    url = f"{BASE_URL}/dashboard/"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200: return True, response.json()
        else: return False, response.json().get("detail", "Authentication failed.")
    except: return False, "Server communication error."

def get_medications(token: str) -> tuple[bool, List[Dict[str, Any]] | str]:
    url = f"{BASE_URL}/medications/"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200: return True, response.json()
        else: return False, response.json().get("detail", "Failed to fetch medications.")
    except: return False, "Server communication error."

def add_medication(token: str, payload: dict) -> tuple[bool, str]:
    url = f"{BASE_URL}/medications/"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201: return True, "Medication added successfully!"
        else: return False, response.json().get("detail", "Failed to add medication.")
    except: return False, "Server communication error."

def delete_medication(token: str, med_id: int) -> tuple[bool, str]:
    url = f"{BASE_URL}/medications/{med_id}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 200: return True, "Medication deleted successfully."
        else: return False, response.json().get("detail", "Failed to delete medication.")
    except: return False, "Server communication error."

# --- THIS FUNCTION IS CORRECTED ---
def mark_medication_as_taken(token: str, med_id: int) -> tuple[bool, str]:
    url = f"{BASE_URL}/medications/{med_id}/taken"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        # The POST request must include the headers
        response = requests.post(url, headers=headers)
        if response.status_code == 200: return True, "Medication marked as taken."
        else: return False, response.json().get("detail", "Failed to mark as taken.")
    except: return False, "Server communication error."

def get_appointments(token: str) -> tuple[bool, List[Dict[str, Any]] | str]:
    url = f"{BASE_URL}/appointments/"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200: return True, response.json()
        else: return False, response.json().get("detail", "Failed to fetch appointments.")
    except: return False, "Server communication error."

def add_appointment(token: str, payload: dict) -> tuple[bool, str]:
    url = f"{BASE_URL}/appointments/"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201: return True, "Appointment added successfully!"
        else:
            detail = response.json().get("detail", "Failed to add appointment.")
            if isinstance(detail, list): detail = " ".join([d.get('msg', '') for d in detail])
            return False, str(detail)
    except: return False, "Server communication error."

def delete_appointment(token: str, appt_id: int) -> tuple[bool, str]:
    url = f"{BASE_URL}/appointments/{appt_id}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 200: return True, "Appointment deleted successfully."
        else: return False, response.json().get("detail", "Failed to delete appointment.")
    except: return False, "Server communication error."

def get_contacts(token: str) -> tuple[bool, List[Dict[str, Any]] | str]:
    url = f"{BASE_URL}/contacts/"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200: return True, response.json()
        else: return False, response.json().get("detail", "Failed to fetch contacts.")
    except: return False, "Server communication error."

def add_contact(token: str, payload: dict) -> tuple[bool, str]:
    url = f"{BASE_URL}/contacts/"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201: return True, "Contact added successfully!"
        else: return False, response.json().get("detail", "Failed to add contact.")
    except: return False, "Server communication error."

def delete_contact(token: str, contact_id: int) -> tuple[bool, str]:
    url = f"{BASE_URL}/contacts/{contact_id}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 200: return True, "Contact deleted successfully."
        else: return False, response.json().get("detail", "Failed to delete contact.")
    except: return False, "Server communication error."

def get_profile(token: str) -> tuple[bool, dict | str]:
    url = f"{BASE_URL}/users/me"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200: return True, response.json()
        else: return False, response.json().get("detail", "Failed to fetch profile.")
    except: return False, "Server communication error."

def update_profile(token: str, payload: dict) -> tuple[bool, str]:
    url = f"{BASE_URL}/users/me"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.put(url, headers=headers, json=payload)
        if response.status_code == 200: return True, "Profile updated successfully!"
        else: return False, response.json().get("detail", "Failed to update profile.")
    except: return False, "Server communication error."

def request_password_reset(email: str) -> tuple[bool, str]:
    url = f"{BASE_URL}/auth/forgot-password"
    payload = {"email": email}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200: return True, response.json().get("msg")
        else: return False, response.json().get("detail", "An unknown error occurred.")
    except: return False, "Server communication error."

def set_new_password(token: str, new_password: str) -> tuple[bool, str]:
    url = f"{BASE_URL}/auth/reset-password"
    payload = {"token": token, "new_password": new_password}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200: return True, response.json().get("msg")
        else: return False, response.json().get("detail", "Failed to reset password.")
    except: return False, "Server communication error."

# --- THIS FUNCTION IS ALSO CORRECTED ---
def add_health_tip(token: str, tip_text: str) -> tuple[bool, str]:
    url = f"{BASE_URL}/tips/"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"tip_text": tip_text}
    try:
        # The POST request must include the headers
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            return True, "Health tip added successfully!"
        else:
            return False, response.json().get("detail", "Failed to add health tip.")
    except: return False, "Server communication error."