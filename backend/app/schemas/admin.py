"""Admin-related schemas."""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class DashboardStats(BaseModel):
    """ADM_03 - Home dashboard."""
    live_trips: int
    online_drivers: int
    open_tickets: int
    pending_kyc: int
    failed_payouts: int
    updated_at: str


class LiveTripItem(BaseModel):
    """ADM_04 - Live trip row."""
    trip_id: str
    driver_name: str
    rider_name: str
    status: str
    eta_mins: Optional[int] = None
    sos_alert: Optional[dict] = None


class KycQueueItem(BaseModel):
    """ADM_05 - Driver KYC queue."""
    driver_id: str
    status: str  # pending | review
    note: Optional[str] = None
    city: Optional[str] = None


class KycActionRequest(BaseModel):
    driver_id: str
    action: str  # approve | reject | hold
    reason: Optional[str] = None


class FleetComplianceStats(BaseModel):
    """ADM_06."""
    active_vehicles: int
    expiring_insurance: int
    fitness_due: int
    blocked: int


class AddVehicleRequest(BaseModel):
    """ADM_06A."""
    vehicle_name: str
    vehicle_type: str  # single | sharing | outstation
    base_fare_inr: float
    per_km_inr: float
    per_min_inr: float


class VehiclePricingUpdate(BaseModel):
    """ADM_06B."""
    vehicle_id: str
    base_fare_inr: float
    per_km_inr: float


class PricingConfig(BaseModel):
    """ADM_07 - Commission & surge."""
    commission_percent: float
    base_fare_index: float
    max_surge: float
    surge_zones_active: int
    city: Optional[str] = None


class LoyaltyConfig(BaseModel):
    """ADM_08 - Martingale loyalty."""
    tiers: List[Dict[str, Any]]  # ride # -> discount %
    cap_per_user_per_day_inr: float
    segments: Optional[List[str]] = None


class PayoutStats(BaseModel):
    """ADM_10."""
    pending_inr: float
    processed_today_inr: float
    failed_transfers: int


class DisputeItem(BaseModel):
    """ADM_11."""
    id: str
    type: str
    trip_id: str
    status: str
    amount_inr: Optional[float] = None
    description: str


class DisputeActionRequest(BaseModel):
    dispute_id: str
    action: str  # approve_refund | reject | escalate
    reason: Optional[str] = None


class ReportStats(BaseModel):
    """ADM_12."""
    dau_riders: int
    completion_rate_percent: float
    admin_users_count: int
    privileged_roles: int
    audit_events_count: int
