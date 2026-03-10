"""Support tickets (PAX_21/22, DRV_20)."""
from fastapi import APIRouter, Header, HTTPException
from typing import Optional
from app.schemas.support import CreateTicketRequest, TicketSummary, TicketDetail

router = APIRouter(prefix="/support", tags=["Support"])


def _get_user_id(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization")
    return "user_9899999921"


@router.get("/categories", summary="Help categories (PAX_21)")
def get_help_categories(authorization: Optional[str] = Header(None)) -> list:
    """List support categories for Create Support Ticket."""
    _get_user_id(authorization)
    return [
        {"id": "trip_issues", "label": "Trip Issues"},
        {"id": "payment_refund", "label": "Payment & Refund"},
        {"id": "account_profile", "label": "Account & Profile"},
        {"id": "safety", "label": "Safety Concerns"},
        {"id": "outstation", "label": "Outstation Booking Help"},
    ]


@router.post("/tickets", summary="Create support ticket (PAX_22)")
def create_ticket(body: CreateTicketRequest, authorization: Optional[str] = Header(None)) -> dict:
    _get_user_id(authorization)
    return {
        "ticket_id": "TKT-1001",
        "trip_id": body.trip_id,
        "issue_type": body.issue_type,
        "status": "open",
        "message": "Ticket created. We will get back to you shortly.",
    }


@router.get("/tickets", summary="List my tickets")
def list_tickets(authorization: Optional[str] = Header(None), limit: int = 20, offset: int = 0) -> list:
    _get_user_id(authorization)
    return [
        {"id": "TKT-1001", "trip_id": "TRP-88231", "issue_type": "fare_mismatch", "status": "open", "created_at": "2026-03-08"},
    ][offset : offset + limit]


@router.get("/tickets/{ticket_id}", summary="Track ticket status")
def get_ticket(ticket_id: str, authorization: Optional[str] = Header(None)) -> dict:
    _get_user_id(authorization)
    return {
        "id": ticket_id,
        "trip_id": "TRP-88231",
        "issue_type": "fare_mismatch",
        "status": "in_progress",
        "description": "Fare was higher than estimated.",
        "created_at": "2026-03-08",
        "replies": [],
    }
