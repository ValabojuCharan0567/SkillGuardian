# utils/firebase_store.py
"""
Firebase storage utilities for SkillGuardian.
"""

import firebase_admin
from firebase_admin import credentials, firestore
import os
import datetime
import uuid

firebase_app = None

def _init_firebase():
    global firebase_app
    if not firebase_admin._apps:
        cred_path = os.getenv("FIREBASE_CREDENTIALS")
        if not cred_path or not os.path.exists(cred_path):
            raise ValueError("FIREBASE_CREDENTIALS env var must point to your Firebase service account JSON file.")
        cred = credentials.Certificate(cred_path)
        firebase_app = firebase_admin.initialize_app(cred)

def save_user_report(user_id: str, data: dict) -> None:
    """
    Saves user analysis data and report to Firebase Firestore.
    Args:
        user_id: Unique identifier for the user (could be session or email).
        data: Dictionary containing user input and generated report.
    Returns:
        None
    """
    try:
        _init_firebase()
        db = firestore.client()
        report_id = str(uuid.uuid4())
        data['timestamp'] = datetime.datetime.utcnow()
        db.collection("users").document(user_id).collection("reports").document(report_id).set(data)
    except Exception as e:
        print(f"[Firebase] Error saving report: {e}")

def get_user_reports(user_id: str):
    """
    Fetches all reports for a given user_id from Firestore, sorted by timestamp descending.
    Args:
        user_id: Unique identifier for the user.
    Returns:
        List of report dicts (may be empty).
    """
    try:
        _init_firebase()
        db = firestore.client()
        reports_ref = db.collection("users").document(user_id).collection("reports").order_by("timestamp", direction=firestore.Query.DESCENDING)
        docs = reports_ref.stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"[Firebase] Error fetching reports: {e}")
        return [] 