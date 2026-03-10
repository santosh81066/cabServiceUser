"""
Firebase Admin SDK: verify ID token from Firebase Phone Auth.
Requires: GOOGLE_APPLICATION_CREDENTIALS (path to service account JSON), FIREBASE_PROJECT_ID.
"""
import os
from typing import Optional

_firebase_app = None


def _get_firebase_app():
    global _firebase_app
    if _firebase_app is not None:
        return _firebase_app
    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    project_id = os.environ.get("FIREBASE_PROJECT_ID")
    if not project_id or not cred_path or not os.path.isfile(cred_path):
        return None
    try:
        import firebase_admin
        from firebase_admin import credentials
        cred = credentials.Certificate(cred_path)
        _firebase_app = firebase_admin.initialize_app(cred, options={"projectId": project_id})
        return _firebase_app
    except Exception as e:
        print(f"[Firebase] Init failed: {e}")
        return None


def verify_firebase_token(id_token: str) -> Optional[dict]:
    """
    Verify Firebase ID token (from Phone Auth). Returns decoded claims or None.
    Claims include: uid, phone_number, firebase.sign_in_provider ('phone').
    """
    app = _get_firebase_app()
    if not app:
        return None
    try:
        from firebase_admin import auth
        decoded = auth.verify_id_token(id_token)
        return decoded
    except Exception as e:
        print(f"[Firebase] verify_id_token error: {e}")
        return None
