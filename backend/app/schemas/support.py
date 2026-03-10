"""Support ticket schemas (user and driver)."""
from pydantic import BaseModel
from typing import Optional


class CreateTicketRequest(BaseModel):
    """PAX_22 / DRV - Create support ticket."""
    trip_id: Optional[str] = None
    issue_type: str  # trip_issues | payment_refund | account_profile | safety | etc.
    description: str
    attachment_url: Optional[str] = None


class TicketSummary(BaseModel):
    id: str
    trip_id: Optional[str] = None
    issue_type: str
    status: str  # open | in_progress | resolved
    created_at: str


class TicketDetail(TicketSummary):
    description: str
    replies: Optional[list] = None
