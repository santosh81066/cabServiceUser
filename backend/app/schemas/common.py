"""Common / shared schemas."""
from pydantic import BaseModel
from typing import Optional
from enum import Enum


class RideType(str, Enum):
    SINGLE = "single"
    SHARING = "sharing"
    OUTSTATION = "outstation"


class TripStatus(str, Enum):
    REQUESTED = "requested"
    DRIVER_ASSIGNED = "driver_assigned"
    DRIVER_ARRIVED = "driver_arrived"
    TRIP_STARTED = "trip_started"
    TRIP_COMPLETED = "trip_completed"
    CANCELLED = "cancelled"


class PaymentMethod(str, Enum):
    UPI = "upi"
    CARD = "card"
    WALLET = "wallet"
    CASH = "cash"


class GenderPref(str, Enum):
    ANY = "any"
    FEMALE_ONLY = "female_only"
    MALE_ONLY = "male_only"
