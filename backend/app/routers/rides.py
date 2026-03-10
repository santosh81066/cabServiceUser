"""Ride booking, fare, trip lifecycle, payment (User flow: PAX_03–PAX_12)."""
from fastapi import APIRouter, Header, HTTPException
from typing import Optional
from app.schemas.ride import (
    BookRideRequest,
    FareEstimate,
    DriverAssignedInfo,
    PaymentRequest,
    PaymentSuccessResponse,
    RateDriverRequest,
)

router = APIRouter(prefix="/rides", tags=["Rides"])


def _get_user_id(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization")
    return "user_9899999921"


@router.post("/fare-estimate", summary="Get fare estimate")
def get_fare_estimate(body: BookRideRequest) -> list:
    estimates = [
        FareEstimate(vehicle_type="mini", base_fare_inr=180, per_km_inr=12, estimated_fare_inr=180, min_fare_inr=180),
        FareEstimate(vehicle_type="sedan", base_fare_inr=245, per_km_inr=15, estimated_fare_inr=245, min_fare_inr=245),
        FareEstimate(vehicle_type="suv", base_fare_inr=320, per_km_inr=18, estimated_fare_inr=320, min_fare_inr=320),
    ]
    return estimates


@router.post("/book", summary="Book ride (PAX_03/04/05)")
def book_ride(body: BookRideRequest, authorization: Optional[str] = Header(None)) -> dict:
    _get_user_id(authorization)
    return {"trip_id": "TRP-88231", "status": "driver_assigned", "message": "Ride booked. Driver will be assigned shortly."}


@router.get("/history", summary="Ride history (PAX_10)")
def list_rides(authorization: Optional[str] = Header(None), limit: int = 20, offset: int = 0) -> list:
    _get_user_id(authorization)
    return [
        {"trip_id": "TRP-88231", "pickup": "Bengaluru Airport", "fare_inr": 420, "date": "08 Mar", "vehicle": "Sedan", "status": "completed"},
        {"trip_id": "TRP-88230", "pickup": "MG Road", "fare_inr": 185, "date": "07 Mar", "vehicle": "Auto Share", "status": "completed"},
        {"trip_id": "TRP-88229", "pickup": "Mysuru", "fare_inr": 980, "date": "06 Mar", "vehicle": "Outstation Share", "status": "completed"},
    ][offset : offset + limit]


@router.get("/{trip_id}", summary="Trip detail (PAX_12)")
def get_trip(trip_id: str, authorization: Optional[str] = Header(None)) -> dict:
    _get_user_id(authorization)
    return {
        "id": trip_id,
        "trip_id": trip_id,
        "pickup_address": "Koramangala, Bengaluru",
        "drop_address": "Kempegowda Airport, Bengaluru",
        "pickup_time": "08:12 AM",
        "drop_time": "08:58 AM",
        "status": "trip_completed",
        "fare_breakup": "Base 220 + Distance 145 + Time 20 - Commission 22% (INR 70) - Loyalty 40 = INR 345",
        "driver_name": "Ravi Kumar",
        "vehicle": "White Swift • KA 01 AB 1234",
    }


@router.get("/{trip_id}/driver", response_model=DriverAssignedInfo, summary="Driver assigned (PAX_06)")
def get_driver_assigned(trip_id: str, authorization: Optional[str] = Header(None)) -> DriverAssignedInfo:
    _get_user_id(authorization)
    return DriverAssignedInfo(
        driver_id="drv_1",
        driver_name="Ravi Kumar",
        rating=4.8,
        vehicle="White Swift",
        vehicle_number="KA 01 AB 1234",
        otp="6421",
        eta_mins=4,
    )


@router.get("/{trip_id}/live", summary="Live trip (PAX_07)")
def get_live_trip(trip_id: str, authorization: Optional[str] = Header(None)) -> dict:
    _get_user_id(authorization)
    return {"trip_id": trip_id, "progress_percent": 72, "eta_mins": 9, "current_fare_inr": 268}


@router.get("/{trip_id}/payment-methods", summary="Payment methods (PAX_08)")
def get_payment_methods(trip_id: str, authorization: Optional[str] = Header(None)) -> list:
    _get_user_id(authorization)
    return [
        {"method": "upi", "display_name": "UPI", "is_available": True},
        {"method": "card", "display_name": "Credit / Debit Card", "is_available": True},
        {"method": "wallet", "display_name": "Wallet Balance (INR 480)", "is_available": True, "wallet_balance": 480},
        {"method": "cash", "display_name": "Cash", "is_available": True},
    ]


@router.post("/{trip_id}/pay", response_model=PaymentSuccessResponse, summary="Pay (PAX_08)")
def pay_trip(trip_id: str, body: PaymentRequest, authorization: Optional[str] = Header(None)) -> PaymentSuccessResponse:
    _get_user_id(authorization)
    return PaymentSuccessResponse(success=True, trip_id=trip_id, amount_paid_inr=body.amount_inr, invoice_url=f"/invoices/{trip_id}")


@router.post("/{trip_id}/rate", summary="Rate driver (PAX_09)")
def rate_driver(trip_id: str, body: RateDriverRequest, authorization: Optional[str] = Header(None)) -> dict:
    _get_user_id(authorization)
    return {"message": "Thank you for your feedback", "trip_id": trip_id}


@router.post("/{trip_id}/cancel", summary="Cancel ride (PAX_06)")
def cancel_ride(trip_id: str, authorization: Optional[str] = Header(None)) -> dict:
    _get_user_id(authorization)
    return {"message": "Ride cancelled", "trip_id": trip_id}
