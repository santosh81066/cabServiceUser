"""Admin APIs: Dashboard, live trips, KYC queue, fleet, pricing, loyalty, payout, disputes (ADM_03–ADM_12)."""
from fastapi import APIRouter, Header, HTTPException
from typing import Optional
from app.schemas.admin import (
    DashboardStats,
    LiveTripItem,
    KycQueueItem,
    KycActionRequest,
    FleetComplianceStats,
    AddVehicleRequest,
    VehiclePricingUpdate,
    PricingConfig,
    LoyaltyConfig,
    PayoutStats,
    DisputeItem,
    DisputeActionRequest,
    ReportStats,
)

router = APIRouter(prefix="/admin", tags=["Admin"])


def _require_admin(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer ") or "admin_token" not in authorization:
        raise HTTPException(status_code=403, detail="Admin access required")
    return "admin"


# ----- Dashboard (ADM_03) -----
@router.get("/dashboard", response_model=DashboardStats, summary="Admin home (ADM_03)")
def get_dashboard(authorization: Optional[str] = Header(None)) -> DashboardStats:
    _require_admin(authorization)
    return DashboardStats(
        live_trips=182,
        online_drivers=948,
        open_tickets=43,
        pending_kyc=126,
        failed_payouts=34,
        updated_at="2026-03-10T10:00:00Z",
    )


# ----- Live trips (ADM_04) -----
@router.get("/live-trips", summary="Live trips monitor (ADM_04)")
def list_live_trips(authorization: Optional[str] = Header(None), limit: int = 50) -> list:
    _require_admin(authorization)
    return [
        {"trip_id": "CTD-5502", "driver_name": "Ravi", "rider_name": "Anand", "status": "on_route", "eta_mins": 7, "sos_alert": None},
        {"trip_id": "SP-338", "driver_name": "-", "rider_name": "-", "status": "sos", "eta_mins": None, "sos_alert": {"level": "high", "location": "Koramangala", "raised_mins_ago": 2}},
    ][:limit]


# ----- Driver KYC (ADM_05) -----
@router.get("/kyc/queue", summary="Driver KYC queue (ADM_05)")
def get_kyc_queue(authorization: Optional[str] = Header(None), status: Optional[str] = None) -> list:
    _require_admin(authorization)
    return [
        {"driver_id": "DRV-9832", "status": "pending", "note": "Aadhaar mismatch", "city": "Bengaluru"},
        {"driver_id": "DRV-7721", "status": "review", "note": "DL image blur", "city": "Mysuru"},
        {"driver_id": "DRV-5504", "status": "pending", "note": "RC doc incomplete", "city": "Chennai"},
    ]


@router.post("/kyc/action", summary="Approve / Reject / Hold KYC (ADM_05)")
def kyc_action(body: KycActionRequest, authorization: Optional[str] = Header(None)) -> dict:
    _require_admin(authorization)
    return {"driver_id": body.driver_id, "action": body.action, "message": f"KYC {body.action} successful"}


# ----- Fleet compliance (ADM_06) -----
@router.get("/fleet/compliance", response_model=FleetComplianceStats, summary="Fleet compliance (ADM_06)")
def get_fleet_compliance(authorization: Optional[str] = Header(None)) -> FleetComplianceStats:
    _require_admin(authorization)
    return FleetComplianceStats(
        active_vehicles=3120,
        expiring_insurance=86,
        fitness_due=47,
        blocked=12,
    )


@router.post("/fleet/compliance/sweep", summary="Run compliance sweep (ADM_06)")
def run_compliance_sweep(authorization: Optional[str] = Header(None)) -> dict:
    _require_admin(authorization)
    return {"message": "Compliance sweep completed", "blocked_count": 0}


# ----- Vehicles (ADM_06A, ADM_06B) -----
@router.post("/vehicles", summary="Add vehicle (ADM_06A)")
def add_vehicle(body: AddVehicleRequest, authorization: Optional[str] = Header(None)) -> dict:
    _require_admin(authorization)
    return {"message": "Vehicle added", "vehicle_id": "v_mini", "name": body.vehicle_name}


@router.get("/vehicles", summary="List vehicles")
def list_vehicles(authorization: Optional[str] = Header(None)) -> list:
    _require_admin(authorization)
    return [
        {"id": "v_mini", "name": "Mini", "base_fare_inr": 40, "per_km_inr": 12},
        {"id": "v_sedan", "name": "Sedan", "base_fare_inr": 60, "per_km_inr": 15},
        {"id": "v_suv", "name": "SUV", "base_fare_inr": 80, "per_km_inr": 18},
    ]


@router.put("/vehicles/pricing", summary="Save vehicle pricing (ADM_06B)")
def save_vehicle_pricing(body: VehiclePricingUpdate, authorization: Optional[str] = Header(None)) -> dict:
    _require_admin(authorization)
    return {"message": "Pricing saved", "vehicle_id": body.vehicle_id}


# ----- Pricing & surge (ADM_07) -----
@router.get("/pricing", summary="Pricing config (ADM_07)")
def get_pricing(authorization: Optional[str] = Header(None)) -> dict:
    _require_admin(authorization)
    return {
        "commission_percent": 22,
        "base_fare_index": 1.0,
        "max_surge": 2.5,
        "surge_zones_active": 7,
        "city": "Bengaluru",
    }


@router.put("/pricing", summary="Publish pricing (ADM_07)")
def update_pricing(body: PricingConfig, authorization: Optional[str] = Header(None)) -> dict:
    _require_admin(authorization)
    return {"message": "Pricing rules published"}


# ----- Loyalty (ADM_08) -----
@router.get("/loyalty", summary="Loyalty engine (ADM_08)")
def get_loyalty_config(authorization: Optional[str] = Header(None)) -> dict:
    _require_admin(authorization)
    return {
        "tiers": [{"ride_number": 1, "discount_percent": 10}, {"ride_number": 2, "discount_percent": 20}, {"ride_number": 4, "discount_percent": 25}, {"ride_number": 8, "discount_percent": 30}, {"ride_number": 16, "discount_percent": 40}],
        "cap_per_user_per_day_inr": 80,
        "segments": ["new", "frequent", "outstation"],
    }


@router.put("/loyalty", summary="Save loyalty config (ADM_08)")
def save_loyalty(body: LoyaltyConfig, authorization: Optional[str] = Header(None)) -> dict:
    _require_admin(authorization)
    return {"message": "Loyalty config saved"}


# ----- Outstation & sharing ops (ADM_09) -----
@router.get("/allocation", summary="Outstation & sharing ops (ADM_09)")
def get_allocation_stats(authorization: Optional[str] = Header(None)) -> dict:
    _require_admin(authorization)
    return {
        "outstation_requests": 264,
        "pool_fill_rate_percent": 78,
        "top_corridor": "BLR-MYS",
        "max_detour_mins": 10,
        "fallback_to_single": True,
    }


@router.post("/allocation/apply", summary="Apply allocation policy (ADM_09)")
def apply_allocation_policy(authorization: Optional[str] = Header(None)) -> dict:
    _require_admin(authorization)
    return {"message": "Allocation policy applied"}


# ----- Payout (ADM_10) -----
@router.get("/payout/stats", summary="Payout stats (ADM_10)")
def get_payout_stats(authorization: Optional[str] = Header(None)) -> dict:
    _require_admin(authorization)
    return {
        "pending_inr": 720000,
        "processed_today_inr": 1890000,
        "failed_transfers": 34,
    }


@router.post("/payout/release", summary="Release payout batch (ADM_10)")
def release_payout_batch(authorization: Optional[str] = Header(None)) -> dict:
    _require_admin(authorization)
    return {"message": "Payout batch released", "batch_id": "PAY-2026-03-10-001"}


@router.post("/payout/retry-failed", summary="Retry failed transfers (ADM_10)")
def retry_failed_payouts(authorization: Optional[str] = Header(None)) -> dict:
    _require_admin(authorization)
    return {"message": "Retry queued for failed transfers"}


# ----- Disputes (ADM_11) -----
@router.get("/disputes", summary="Disputes & refunds (ADM_11)")
def list_disputes(authorization: Optional[str] = Header(None), status: Optional[str] = None) -> list:
    _require_admin(authorization)
    return [
        {"id": "d1", "type": "fare_mismatch", "trip_id": "CTD-4451", "status": "high", "amount_inr": 120, "description": "Refund INR 120 requested"},
        {"id": "d2", "type": "no_show_conflict", "trip_id": "CTD-7710", "status": "open", "amount_inr": None, "description": "Driver/rider dispute"},
    ]


@router.post("/disputes/action", summary="Approve refund / Reject / Escalate (ADM_11)")
def dispute_action(body: DisputeActionRequest, authorization: Optional[str] = Header(None)) -> dict:
    _require_admin(authorization)
    return {"dispute_id": body.dispute_id, "action": body.action, "message": "Action recorded"}


# ----- Reports & access (ADM_12) -----
@router.get("/reports/stats", summary="Reports (ADM_12)")
def get_report_stats(authorization: Optional[str] = Header(None)) -> dict:
    _require_admin(authorization)
    return {
        "dau_riders": 82000,
        "completion_rate_percent": 92,
        "admin_users_count": 54,
        "privileged_roles": 7,
        "audit_events_count": 4300,
    }


@router.get("/reports/city-revenue", summary="City revenue report (ADM_12)")
def get_city_revenue_report(authorization: Optional[str] = Header(None), city: Optional[str] = None) -> dict:
    _require_admin(authorization)
    return {"city": city or "Bengaluru", "period": "month", "revenue_inr": 12500000, "trips": 45000}
