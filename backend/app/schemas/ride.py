"""Ride / trip related schemas (user booking, fare, driver assignment)."""
from pydantic import BaseModel
from typing import Optional, List
from .common import RideType, GenderPref, TripStatus


class LocationInput(BaseModel):
    latitude: float
    longitude: float
    address: Optional[str] = None


class BookRideRequest(BaseModel):
    """PAX_03, PAX_04, PAX_05 - Book ride (single / sharing / outstation)."""
    ride_type: RideType
    pickup: LocationInput
    drop: LocationInput
    vehicle_type: str  # mini, sedan, suv, bike_pool, auto_share, mini_share, etc.
    stops: Optional[List[LocationInput]] = None
    schedule_at: Optional[str] = None  # ISO datetime if scheduled
    # Sharing
    seats: Optional[int] = 1
    max_detour_mins: Optional[int] = None
    gender_pref: Optional[GenderPref] = GenderPref.ANY
    # Outstation
    from_city: Optional[str] = None
    to_city: Optional[str] = None
    departure_date: Optional[str] = None
    departure_time: Optional[str] = None
    trip_type: Optional[str] = "one_way"  # one_way | round_trip
    luggage: Optional[str] = None  # small | medium | large


class FareEstimate(BaseModel):
    """Fare estimate for vehicle selection."""
    vehicle_type: str
    base_fare_inr: float
    per_km_inr: float
    estimated_fare_inr: float
    min_fare_inr: Optional[float] = None


class TripSummary(BaseModel):
    """Trip card for list/detail views."""
    id: str
    trip_id: str  # e.g. TRP-88231
    pickup_address: str
    drop_address: str
    status: TripStatus
    vehicle_type: str
    fare_inr: Optional[float] = None
    completed_at: Optional[str] = None
    driver_name: Optional[str] = None
    driver_rating: Optional[float] = None
    driver_vehicle: Optional[str] = None
    driver_otp: Optional[str] = None


class DriverAssignedInfo(BaseModel):
    """PAX_06 - Driver assigned to ride."""
    driver_id: str
    driver_name: str
    rating: float
    vehicle: str
    vehicle_number: str
    otp: str
    eta_mins: int
    phone: Optional[str] = None


class LiveTripUpdate(BaseModel):
    """PAX_07 - Live trip progress."""
    trip_id: str
    progress_percent: float
    eta_mins: int
    current_fare_inr: float


class PaymentMethodOption(BaseModel):
    """PAX_08 - Payment option."""
    method: str  # upi | card | wallet | cash
    display_name: str
    is_available: bool
    wallet_balance: Optional[float] = None


class PaymentRequest(BaseModel):
    """PAX_08 - Initiate payment."""
    trip_id: str
    method: str  # upi | card | wallet | cash
    amount_inr: float
    upi_id: Optional[str] = None


class PaymentSuccessResponse(BaseModel):
    """PAX_09 - Payment success."""
    success: bool
    trip_id: str
    amount_paid_inr: float
    invoice_url: Optional[str] = None


class RateDriverRequest(BaseModel):
    """PAX_09 - Rate driver after trip."""
    trip_id: str
    rating: int  # 1-5
    comment: Optional[str] = None
