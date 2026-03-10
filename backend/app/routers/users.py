"""User (passenger) APIs - profile, wallet, saved places, coupons, referral, notifications."""
from fastapi import APIRouter, Header, HTTPException
from typing import Optional
from app.schemas.user import (
    UserProfile,
    UserProfileUpdate,
    WalletBalance,
    AddMoneyRequest,
    ReferralInfo,
    NotificationPrefs,
)

router = APIRouter(prefix="/users", tags=["User (Passenger)"])


def _get_user_id(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization")
    return "user_9899999921"


@router.get("/me", response_model=UserProfile, summary="My profile (PAX_14)")
def get_my_profile(authorization: Optional[str] = Header(None)) -> UserProfile:
    _get_user_id(authorization)
    return UserProfile(
        name="Santosh Kumar",
        phone="+91 98XXXXXX21",
        email="santosh@mail.com",
        gender="Male",
        preferred_language="English",
    )


@router.patch("/me", response_model=UserProfile, summary="Edit profile (PAX_11)")
def update_profile(body: UserProfileUpdate, authorization: Optional[str] = Header(None)) -> UserProfile:
    _get_user_id(authorization)
    return UserProfile(
        name=body.name or "Santosh Kumar",
        phone="+91 98XXXXXX21",
        email=body.email,
        gender=body.gender,
        preferred_language=body.preferred_language or "English",
    )


@router.get("/wallet", response_model=WalletBalance, summary="Wallet balance (PAX_16)")
def get_wallet(authorization: Optional[str] = Header(None)) -> WalletBalance:
    _get_user_id(authorization)
    return WalletBalance(balance_inr=480.0)


@router.get("/wallet/transactions", summary="Wallet transactions (PAX_16)")
def get_wallet_transactions(authorization: Optional[str] = Header(None), limit: int = 20, offset: int = 0) -> list:
    _get_user_id(authorization)
    return [
        {"id": "1", "type": "credit", "amount_inr": 500, "description": "Added via UPI", "created_at": "2026-03-07"},
        {"id": "2", "type": "debit", "amount_inr": -120, "description": "Ride Fare Deduction", "created_at": "2026-03-06"},
    ][offset : offset + limit]


@router.post("/wallet/add-money", summary="Add money (PAX_17)")
def add_money(body: AddMoneyRequest, authorization: Optional[str] = Header(None)) -> dict:
    _get_user_id(authorization)
    return {"message": "Redirect to payment", "amount_inr": body.amount_inr, "payment_method": body.payment_method, "order_id": "wm_001"}


@router.get("/saved-places", summary="Saved places (PAX_24)")
def get_saved_places(authorization: Optional[str] = Header(None)) -> list:
    _get_user_id(authorization)
    return [
        {"id": "1", "label": "Home", "address": "HSR Layout, Bengaluru", "is_primary": True},
        {"id": "2", "label": "Work", "address": "Embassy Tech Park, Bengaluru", "is_primary": True},
        {"id": "3", "label": "Gym", "address": "Koramangala, Bengaluru", "is_primary": False},
    ]


@router.post("/saved-places", summary="Add saved place")
def add_saved_place(body: dict, authorization: Optional[str] = Header(None)) -> dict:
    _get_user_id(authorization)
    return {"id": "4", "label": body.get("label"), "address": body.get("address"), "is_primary": False}


@router.post("/coupons/apply", summary="Apply coupon (PAX_18)")
def apply_coupon(body: dict, authorization: Optional[str] = Header(None)) -> dict:
    _get_user_id(authorization)
    return {"applied": True, "coupon_code": body.get("coupon_code"), "discount_inr": 25, "message": "Coupon applied successfully"}


@router.get("/coupons/available", summary="Available coupons (PAX_18)")
def get_available_coupons(authorization: Optional[str] = Header(None)) -> list:
    _get_user_id(authorization)
    return [
        {"code": "WELCOME10", "discount_inr": 25, "description": "Valid on first 3 rides"},
        {"code": "SHARE20", "discount_inr": 20, "description": "Valid for sharing rides"},
        {"code": "OUTCITY50", "discount_inr": 50, "description": "Valid for outstation booking"},
    ]


@router.get("/referral", response_model=ReferralInfo, summary="Refer & earn (PAX_19)")
def get_referral(authorization: Optional[str] = Header(None)) -> ReferralInfo:
    _get_user_id(authorization)
    return ReferralInfo(referral_code="SANTOSH21", friends_joined=3, earnings_inr=180.0)


@router.get("/notifications/preferences", summary="Notification prefs (PAX_25)")
def get_notification_prefs(authorization: Optional[str] = Header(None)) -> NotificationPrefs:
    _get_user_id(authorization)
    return NotificationPrefs(trip_alerts=True, promo_offers=True, outstation_deals=False, payment_reminders=True, sms_notifications=True)


@router.put("/notifications/preferences", summary="Save notification prefs")
def save_notification_prefs(body: NotificationPrefs, authorization: Optional[str] = Header(None)) -> dict:
    _get_user_id(authorization)
    return {"message": "Preferences saved"}


# ----- Discount / reward progress (PAX_13, PAX_20) -----
@router.get("/discounts/history", summary="Discount history - Martingale (PAX_13)")
def get_discount_history(authorization: Optional[str] = Header(None)) -> list:
    _get_user_id(authorization)
    return [
        {"ride_number": 4, "coupon": "-25%", "applied_at": "08 Mar 2026"},
        {"ride_number": 2, "coupon": "-20%", "applied_at": "05 Mar 2026"},
        {"ride_number": 1, "coupon": "-10%", "applied_at": "03 Mar 2026"},
    ]


@router.get("/rewards/progress", summary="Reward progress - Martingale (PAX_20)")
def get_reward_progress(authorization: Optional[str] = Header(None)) -> dict:
    _get_user_id(authorization)
    return {
        "completed_rides": 5,
        "next_coupon_at_ride": 8,
        "last_coupon": "Ride #4 (-25%)",
        "saved_inr": 40,
        "progress_percent": 66,
    }
