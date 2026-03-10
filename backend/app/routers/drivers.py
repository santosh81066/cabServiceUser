"""Driver APIs: KYC, ride requests, trip flow, earnings, payout, incentives (DRV_03–DRV_22)."""
from fastapi import APIRouter, Header, HTTPException
from typing import Optional
from app.schemas.driver import (
    KycStatus,
    AadhaarVerifyRequest,
    DrivingLicenseRequest,
    RcVerifyRequest,
    InsuranceRequest,
    BankVerifyRequest,
    ServiceSetupRequest,
    RideRequestCard,
    AcceptRejectRequest,
    StartTripOtpRequest,
    DriverEarnings,
    PayoutRequest,
    IncentiveSummary,
    DriverProfile,
    DriverSettingsUpdate,
)
from app.schemas.common import RideType

router = APIRouter(prefix="/drivers", tags=["Driver"])


def _get_driver_id(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization")
    return "driver_9899999954"


# ----- KYC (DRV_03, DRV_03A–G) -----
@router.get("/kyc/status", response_model=KycStatus, summary="KYC home (DRV_03)")
def get_kyc_status(authorization: Optional[str] = Header(None)) -> KycStatus:
    _get_driver_id(authorization)
    return KycStatus(
        aadhaar="pending",
        driving_license="pending",
        rc_book="pending",
        vehicle_insurance="pending",
        bank_payout="pending",
        profile_completion_percent=20,
    )


@router.post("/kyc/aadhaar", summary="Aadhaar verification (DRV_03A)")
def verify_aadhaar(body: AadhaarVerifyRequest, authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {"message": "Aadhaar verified", "next_step": "driving_license"}


@router.post("/kyc/driving-license", summary="Driving license (DRV_03B)")
def submit_dl(body: DrivingLicenseRequest, authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {"message": "DL uploaded", "next_step": "rc_book"}


@router.post("/kyc/rc", summary="RC book (DRV_03C)")
def submit_rc(body: RcVerifyRequest, authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {"message": "RC uploaded", "next_step": "insurance"}


@router.post("/kyc/insurance", summary="Insurance (DRV_03D)")
def submit_insurance(body: InsuranceRequest, authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {"message": "Insurance saved", "next_step": "bank"}


@router.post("/kyc/bank", summary="Bank & payout (DRV_03E)")
def verify_bank(body: BankVerifyRequest, authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {"message": "Bank verified", "next_step": "review"}


@router.post("/kyc/submit", summary="Submit KYC for approval (DRV_03F)")
def submit_kyc(authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {"message": "KYC submitted for approval", "status": "pending"}


# ----- Service setup (DRV_04) -----
@router.put("/service-setup", summary="Vehicle & service setup (DRV_04)")
def save_service_setup(body: ServiceSetupRequest, authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {"message": "Service setup saved", "can_go_online": True}


# ----- Home & ride requests (DRV_05–08) -----
@router.get("/home", summary="Driver home (DRV_05)")
def driver_home(authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {
        "status": "online",
        "earnings_today_inr": 2480,
        "wallet_balance_inr": 760,
        "completed_trips_today": 6,
        "acceptance_rate": 92,
        "cancel_rate": 2.1,
        "pending_request": None,
    }


@router.get("/requests/pending", summary="Pending ride request (DRV_06/07/08)")
def get_pending_request(authorization: Optional[str] = Header(None)) -> dict | None:
    """New request appears on home. Returns one pending request or null."""
    _get_driver_id(authorization)
    return {
        "request_id": "req_001",
        "ride_type": "single",
        "pickup_address": "MG Road Metro",
        "drop_address": "Indiranagar 100ft Rd",
        "fare_inr": 310,
        "distance_to_pickup_km": 0.9,
        "eta_mins": 3,
    }


@router.post("/requests/respond", summary="Accept or reject (DRV_06/07/08)")
def respond_to_request(body: AcceptRejectRequest, authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {"accepted": body.accept, "request_id": body.request_id, "trip_id": "TRP-88231" if body.accept else None}


# ----- Trip flow (DRV_09–14) -----
@router.post("/trips/{trip_id}/arrived", summary="Arrived at pickup (DRV_10)")
def mark_arrived(trip_id: str, authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {"trip_id": trip_id, "status": "driver_arrived", "wait_timer_started": True}


@router.post("/trips/start", summary="Verify OTP & start trip (DRV_11)")
def start_trip(body: StartTripOtpRequest, authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {"trip_id": body.trip_id, "status": "trip_started", "message": "Trip started"}


@router.post("/trips/{trip_id}/complete", summary="Reached destination (DRV_12/13)")
def complete_trip(trip_id: str, authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {
        "trip_id": trip_id,
        "status": "trip_completed",
        "driver_earning_inr": 214,
        "total_fare_inr": 285,
        "next_step": "collect_payment",
    }


@router.post("/trips/{trip_id}/payment-collected", summary="Mark payment collected (DRV_14)")
def mark_payment_collected(trip_id: str, authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {"trip_id": trip_id, "message": "Payment marked as collected", "wallet_credited": True}


@router.post("/trips/{trip_id}/no-show", summary="Mark rider no-show (DRV_10)")
def mark_no_show(trip_id: str, authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {"trip_id": trip_id, "status": "cancelled", "reason": "no_show"}


# ----- Earnings & payout (DRV_15, DRV_16) -----
@router.get("/earnings", summary="Earnings & wallet (DRV_15)")
def get_earnings(authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {
        "wallet_balance_inr": 4820,
        "today_earnings_inr": 2480,
        "week_earnings_inr": 14230,
        "completed_trips_today": 9,
        "average_trip_earning_inr": 276,
        "recent_trips": [
            {"trip_id": "CTD-5502", "earning_inr": 214, "type": "Single", "date": "7 Mar"},
            {"trip_id": "CTD-5498", "earning_inr": 332, "type": "Outstation Share", "date": "7 Mar"},
        ],
    }


@router.post("/payout", summary="Transfer to bank (DRV_16)")
def request_payout(body: PayoutRequest, authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {
        "message": "Transfer initiated",
        "amount_inr": body.amount_inr,
        "charge_inr": 5,
        "expected_credit": "2 hours",
    }


# ----- Incentives (DRV_17) -----
@router.get("/incentives", summary="Incentives & targets (DRV_17)")
def get_incentives(authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {
        "daily_target_trips": 12,
        "daily_completed_trips": 9,
        "daily_bonus_inr": 500,
        "weekly_target_trips": 50,
        "weekly_completed_trips": 42,
        "weekly_bonus_inr": 1800,
        "outstation_mission": {"required": 3, "completed": 2, "bonus_inr": 500},
    }


# ----- Ride history (DRV_18) -----
@router.get("/rides/history", summary="Ride history (DRV_18)")
def ride_history(authorization: Optional[str] = Header(None), limit: int = 20, offset: int = 0) -> list:
    _get_driver_id(authorization)
    return [
        {"trip_id": "CTD-5502", "date": "7 Mar", "status": "completed", "type": "Single", "earning_inr": 214},
        {"trip_id": "CTD-5498", "date": "7 Mar", "status": "completed", "type": "Outstation Share", "earning_inr": 332},
        {"trip_id": "CTD-5481", "date": "6 Mar", "status": "cancelled", "note": "No-show at pickup", "compensation_inr": 25},
    ][offset : offset + limit]


# ----- Ratings (DRV_19) -----
@router.get("/ratings", summary="Ratings & feedback (DRV_19)")
def get_ratings(authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {
        "overall_rating": 4.8,
        "politeness": 4.9,
        "driving_safety": 4.8,
        "cleanliness": 4.7,
        "recent_reviews": [{"rating": 5, "comment": "Very smooth ride and on-time pickup.", "trip_id": "CTD-5502"}],
    }


# ----- Help (DRV_20) -----
@router.get("/help/categories", summary="Help & emergency (DRV_20)")
def help_categories(authorization: Optional[str] = Header(None)) -> list:
    _get_driver_id(authorization)
    return [
        {"id": "emergency_sos", "label": "Emergency SOS"},
        {"id": "driver_support", "label": "Call Driver Support"},
        {"id": "rider_misconduct", "label": "Report Rider Misconduct"},
        {"id": "payment_dispute", "label": "Payment Dispute"},
    ]


# ----- Profile & settings (DRV_21, DRV_22) -----
@router.get("/profile", response_model=DriverProfile, summary="Profile (DRV_21)")
def get_profile(authorization: Optional[str] = Header(None)) -> DriverProfile:
    _get_driver_id(authorization)
    return DriverProfile(
        driver_id="drv_1",
        name="Ravi Kumar",
        phone="+91 98XXXXXX54",
        vehicle_details={"vehicle": "White Swift", "number": "KA 01 AB 1234"},
        kyc_status="verified",
        rating=4.8,
    )


@router.get("/settings", summary="Settings (DRV_22)")
def get_settings(authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {
        "online_auto_accept": False,
        "outstation_requests": True,
        "sharing_requests": True,
        "night_shift_mode": False,
        "language": "en",
        "notification_sounds": True,
    }


@router.put("/settings", summary="Update settings (DRV_22)")
def update_settings(body: DriverSettingsUpdate, authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {"message": "Settings updated"}


@router.post("/go-online", summary="Go online")
def go_online(authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {"status": "online", "message": "You are now online"}


@router.post("/go-offline", summary="Go offline (DRV_05)")
def go_offline(authorization: Optional[str] = Header(None)) -> dict:
    _get_driver_id(authorization)
    return {"status": "offline", "message": "You are now offline"}
