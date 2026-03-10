"""Auth-related request/response schemas."""
from pydantic import BaseModel, EmailStr
from typing import Optional


class SendOtpRequest(BaseModel):
    """PAX_01 / DRV_01 - Login with phone."""
    phone: str
    country_code: str = "+91"
    referral_code: Optional[str] = None  # optional referral/promo (user) or fleet ID (driver)


class VerifyOtpRequest(BaseModel):
    """PAX_02 / DRV_02 - Verify OTP."""
    phone: str
    country_code: str = "+91"
    otp: str


class AdminLoginRequest(BaseModel):
    """ADM_01 - Admin login (email + password, no OTP)."""
    email: EmailStr
    password: str


class FirebaseLoginRequest(BaseModel):
    """Firebase Phone Auth: send the ID token from Firebase client after OTP verification."""
    id_token: str


class TokenResponse(BaseModel):
    """JWT / session token response."""
    access_token: str
    token_type: str = "bearer"
    user_id: Optional[str] = None
    role: str  # user | driver | admin
    is_new_user: Optional[bool] = None  # True on first login (Firebase); app can show onboarding
