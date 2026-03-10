"""Driver-related schemas (KYC, trips, earnings, payout)."""
from pydantic import BaseModel
from typing import Optional, List
from .common import RideType, GenderPref


class KycStatus(BaseModel):
    """DRV_03 - KYC tracker."""
    aadhaar: str  # pending | verified
    driving_license: str
    rc_book: str
    vehicle_insurance: str
    bank_payout: str
    profile_completion_percent: int


class AadhaarVerifyRequest(BaseModel):
    """DRV_03A."""
    aadhaar_number: str
    full_name: str
    date_of_birth: str
    otp: str


class DrivingLicenseRequest(BaseModel):
    """DRV_03B."""
    dl_number: str
    issue_date: str
    expiry_date: str
    dl_front_url: Optional[str] = None
    dl_back_url: Optional[str] = None


class RcVerifyRequest(BaseModel):
    """DRV_03C."""
    vehicle_number: str
    owner_name: str
    rc_front_url: Optional[str] = None
    rc_back_url: Optional[str] = None


class InsuranceRequest(BaseModel):
    """DRV_03D."""
    policy_number: str
    provider: str
    expiry_date: str
    document_url: Optional[str] = None


class BankVerifyRequest(BaseModel):
    """DRV_03E."""
    account_holder_name: str
    account_number: str
    ifsc_code: str
    upi_id: Optional[str] = None
    cheque_url: Optional[str] = None


class ServiceSetupRequest(BaseModel):
    """DRV_04 - Vehicle & service setup."""
    vehicle_id: str
    active_categories: List[RideType]  # single, sharing, outstation
    sharing_pref: GenderPref = GenderPref.ANY
    max_seats: int = 3
    luggage: str = "medium"


class RideRequestCard(BaseModel):
    """DRV_05/06/07/08 - Incoming ride request on driver home."""
    request_id: str
    ride_type: RideType
    pickup_address: str
    drop_address: str
    fare_inr: float
    distance_to_pickup_km: Optional[float] = None
    eta_mins: Optional[int] = None
    seats_requested: Optional[int] = None
    gender_pref: Optional[str] = None
    detour_mins: Optional[int] = None
    from_city: Optional[str] = None
    to_city: Optional[str] = None
    pickup_time: Optional[str] = None


class AcceptRejectRequest(BaseModel):
    """Accept or reject ride."""
    request_id: str
    accept: bool


class StartTripOtpRequest(BaseModel):
    """DRV_11 - Verify OTP to start trip."""
    trip_id: str
    otp: str


class DriverEarnings(BaseModel):
    """DRV_15 - Earnings & wallet."""
    wallet_balance_inr: float
    today_earnings_inr: float
    week_earnings_inr: float
    completed_trips_today: int
    average_trip_earning_inr: float
    recent_trips: List[dict]


class PayoutRequest(BaseModel):
    """DRV_16 - Transfer to bank."""
    amount_inr: float


class IncentiveSummary(BaseModel):
    """DRV_17 - Incentives & targets."""
    daily_target_trips: int
    daily_completed_trips: int
    daily_bonus_inr: float
    weekly_target_trips: int
    weekly_completed_trips: int
    weekly_bonus_inr: float
    outstation_mission: Optional[dict] = None


class DriverProfile(BaseModel):
    """DRV_21 - Profile & documents."""
    driver_id: str
    name: str
    phone: str
    vehicle_details: Optional[dict] = None
    kyc_status: str
    rating: Optional[float] = None


class DriverSettingsUpdate(BaseModel):
    """DRV_22 - Settings."""
    online_auto_accept: Optional[bool] = None
    outstation_requests: Optional[bool] = None
    sharing_requests: Optional[bool] = None
    night_shift_mode: Optional[bool] = None
    language: Optional[str] = None
    notification_sounds: Optional[bool] = None
