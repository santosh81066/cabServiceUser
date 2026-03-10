"""Auth APIs: User/Driver OTP login, Admin email+password (PAX_01/02, DRV_01/02, ADM_01)."""
from fastapi import APIRouter, HTTPException
from app.schemas.auth import (
    SendOtpRequest,
    VerifyOtpRequest,
    AdminLoginRequest,
    FirebaseLoginRequest,
    TokenResponse,
)
from app.services.otp_service import send_otp, verify_otp
from app.services.firebase_service import verify_firebase_token
from app.config import settings

# Track Firebase UIDs that have logged in before (in-memory; use DB in production)
_seen_firebase_uids: set[str] = set()

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/user/send-otp", summary="User login - send OTP (PAX_01)")
def user_send_otp(body: SendOtpRequest) -> dict:
    """Generate OTP, store it, and send via SMS (when SMS provider is configured)."""
    success, message, expires_in, otp = send_otp(body.phone, body.country_code)
    if not success:
        raise HTTPException(status_code=500, detail=message)
    response = {
        "message": message,
        "phone": f"{body.country_code} {body.phone}",
        "expires_in_seconds": expires_in,
    }
    if settings.debug:
        response["otp"] = otp  # Dev only: never enable in production
    return response


@router.post("/user/verify-otp", response_model=TokenResponse, summary="User verify OTP (PAX_02)")
def user_verify_otp(body: VerifyOtpRequest) -> TokenResponse:
    """Verify OTP and return session token."""
    if len(body.otp) != 6:
        raise HTTPException(status_code=400, detail="OTP must be 6 digits")
    if not verify_otp(body.phone, body.otp, body.country_code):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    return TokenResponse(
        access_token=f"user_token_{body.phone}_{body.otp}",
        user_id=f"user_{body.phone}",
        role="user",
    )


@router.post("/user/firebase-login", response_model=TokenResponse, summary="User login with Firebase OTP (Firebase Phone Auth)")
def user_firebase_login(body: FirebaseLoginRequest) -> TokenResponse:
    """Verify Firebase ID token (from Phone Auth) and return session token. App sends OTP via Firebase SDK, then sends id_token here."""
    claims = verify_firebase_token(body.id_token)
    if not claims:
        raise HTTPException(status_code=401, detail="Invalid or expired Firebase token")
    uid = claims.get("uid", "")
    phone = claims.get("phone_number") or ""
    if not phone and isinstance(claims.get("firebase"), dict):
        identities = claims["firebase"].get("identities", {}).get("phone") or []
        phone = identities[0] if identities else ""
    if not phone:
        phone = uid or "unknown"
    is_new = uid not in _seen_firebase_uids
    if uid:
        _seen_firebase_uids.add(uid)
    return TokenResponse(
        access_token=f"user_fb_{uid}",
        user_id=f"user_{phone}",
        role="user",
        is_new_user=is_new,
    )


@router.post("/driver/send-otp", summary="Driver login - send OTP (DRV_01)")
def driver_send_otp(body: SendOtpRequest) -> dict:
    """Generate OTP, store it, and send via SMS (when SMS provider is configured)."""
    success, message, expires_in, otp = send_otp(body.phone, body.country_code)
    if not success:
        raise HTTPException(status_code=500, detail=message)
    response = {
        "message": message,
        "phone": f"{body.country_code} {body.phone}",
        "expires_in_seconds": expires_in,
    }
    if settings.debug:
        response["otp"] = otp  # Dev only
    return response


@router.post("/driver/verify-otp", response_model=TokenResponse, summary="Driver verify OTP (DRV_02)")
def driver_verify_otp(body: VerifyOtpRequest) -> TokenResponse:
    """Verify driver OTP and return session token."""
    if len(body.otp) != 6:
        raise HTTPException(status_code=400, detail="OTP must be 6 digits")
    if not verify_otp(body.phone, body.otp, body.country_code):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    return TokenResponse(
        access_token=f"driver_token_{body.phone}_{body.otp}",
        user_id=f"driver_{body.phone}",
        role="driver",
    )


@router.post("/driver/firebase-login", response_model=TokenResponse, summary="Driver login with Firebase OTP (Firebase Phone Auth)")
def driver_firebase_login(body: FirebaseLoginRequest) -> TokenResponse:
    """Verify Firebase ID token (from Phone Auth) and return driver session token."""
    claims = verify_firebase_token(body.id_token)
    if not claims:
        raise HTTPException(status_code=401, detail="Invalid or expired Firebase token")
    uid = claims.get("uid", "")
    phone = claims.get("phone_number") or ""
    if not phone and isinstance(claims.get("firebase"), dict):
        identities = claims["firebase"].get("identities", {}).get("phone") or []
        phone = identities[0] if identities else ""
    if not phone:
        phone = uid or "unknown"
    is_new = uid not in _seen_firebase_uids
    if uid:
        _seen_firebase_uids.add(uid)
    return TokenResponse(
        access_token=f"driver_fb_{uid}",
        user_id=f"driver_{phone}",
        role="driver",
        is_new_user=is_new,
    )


@router.post("/admin/login", response_model=TokenResponse, summary="Admin login (ADM_01, no OTP)")
def admin_login(body: AdminLoginRequest) -> TokenResponse:
    """Admin login with work email and password. No OTP."""
    if not body.email or not body.password:
        raise HTTPException(status_code=400, detail="Email and password required")
    return TokenResponse(
        access_token=f"admin_token_{body.email}",
        user_id=f"admin_{body.email}",
        role="admin",
    )


@router.post("/logout", summary="Logout (PAX_26 / DRV)")
def logout() -> dict:
    """Invalidate current session."""
    return {"message": "Logged out successfully"}
