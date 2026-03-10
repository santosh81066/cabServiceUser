"""User (passenger) related schemas."""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from .common import RideType, GenderPref, PaymentMethod


class UserProfile(BaseModel):
    """PAX_11 / PAX_14 - Profile fields."""
    name: str
    phone: str
    email: Optional[EmailStr] = None
    gender: Optional[str] = None
    preferred_language: Optional[str] = "en"


class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[str] = None
    preferred_language: Optional[str] = None


class WalletBalance(BaseModel):
    """PAX_16 - Wallet balance and meta."""
    balance_inr: float
    currency: str = "INR"


class WalletTransaction(BaseModel):
    """Wallet transaction entry."""
    id: str
    type: str  # credit | debit
    amount_inr: float
    description: str
    created_at: str


class AddMoneyRequest(BaseModel):
    """PAX_17 - Add money to wallet."""
    amount_inr: float
    payment_method: PaymentMethod


class SavedPlace(BaseModel):
    """PAX_24 - Saved place."""
    id: str
    label: str  # Home | Work | Gym etc
    address: str
    is_primary: bool = False


class ApplyCouponRequest(BaseModel):
    """PAX_18 - Apply coupon."""
    coupon_code: str
    trip_id: Optional[str] = None


class CouponInfo(BaseModel):
    """Coupon display."""
    code: str
    discount_type: str  # fixed | percent
    discount_value: float
    description: str
    valid_for: Optional[str] = None


class ReferralInfo(BaseModel):
    """PAX_19 - Refer & earn."""
    referral_code: str
    friends_joined: int
    earnings_inr: float


class NotificationPrefs(BaseModel):
    """PAX_25 - Notification preferences."""
    trip_alerts: bool = True
    promo_offers: bool = True
    outstation_deals: bool = False
    payment_reminders: bool = True
    sms_notifications: bool = True
