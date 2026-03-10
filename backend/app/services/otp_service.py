"""
OTP service: generate OTP, store for verification, and send via SMS.
Set TWILIO_* or MSG91_AUTH_KEY in env to enable real SMS. See README.
"""
import random
import string
from datetime import datetime, timedelta

# In-memory store for development. Use Redis/DB in production.
_otp_store: dict[str, tuple[str, datetime]] = {}
OTP_EXPIRY_SECONDS = 180  # 3 minutes
OTP_LENGTH = 6


def _generate_otp() -> str:
    return "".join(random.choices(string.digits, k=OTP_LENGTH))


def _send_sms(phone: str, message: str) -> bool:
    """
    Send SMS. Priority: Twilio → MSG91 → Gammu (free, open source) → log only.
    """
    import os

    # Option 1: Twilio (pip install twilio)
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_number = os.environ.get("TWILIO_PHONE_NUMBER")
    if account_sid and auth_token and from_number:
        try:
            from twilio.rest import Client
            client = Client(account_sid, auth_token)
            to = phone.replace(" ", "").strip()
            if not to.startswith("+"):
                to = f"+{to}"
            client.messages.create(body=message, from_=from_number, to=to)
            return True
        except Exception as e:
            print(f"[OTP] Twilio error: {e}")
            return False

    # Option 2: MSG91 SendOTP (India) - https://msg91.com
    auth_key = os.environ.get("MSG91_AUTH_KEY")
    if auth_key:
        try:
            import urllib.request
            to = phone.replace(" ", "").replace("+", "").strip()
            if len(to) == 10:
                to = f"91{to}"
            otp = message.split("OTP is ")[1].split(".")[0].strip()
            url = f"https://control.msg91.com/api/sendotp.php?authkey={auth_key}&mobile={to}&otp={otp}"
            with urllib.request.urlopen(url, timeout=10) as r:
                out = r.read().decode()
                if "error" in out.lower() and "success" not in out.lower():
                    print(f"[OTP] MSG91: {out}")
                    return False
                return True
        except Exception as e:
            print(f"[OTP] MSG91 error: {e}")
            return False

    # Option 3: Gammu (free, open source) - USB GSM modem + SIM, pip install python-gammu
    gammu_device = os.environ.get("GAMMU_DEVICE")
    if gammu_device:
        try:
            import gammu
            import tempfile
            with tempfile.NamedTemporaryFile(mode="w", suffix=".rc", delete=False) as f:
                f.write(f"[gammu]\nDevice = {gammu_device}\nConnection = at\n")
                config_path = f.name
            try:
                sm = gammu.StateMachine()
                sm.ReadConfig(Filename=config_path)
                sm.Init()
                to = phone.replace(" ", "").replace("+", "").strip()
                if not to.startswith("91") and len(to) == 10:
                    to = f"91{to}"
                sm.SendSMS(0, {"Number": to, "Text": message, "SMSC": {"Location": 1}})
                return True
            finally:
                try:
                    os.unlink(config_path)
                except Exception:
                    pass
        except ImportError:
            print("[OTP] GAMMU_DEVICE set but python-gammu not installed. pip install python-gammu")
            return False
        except Exception as e:
            print(f"[OTP] Gammu error: {e}")
            return False

    # No provider configured: dev log only
    print(f"[OTP] Would send SMS to {phone}: {message}")
    return True


def send_otp(phone: str, country_code: str = "+91") -> tuple[bool, str, int, str]:
    """
    Generate OTP, store it, and optionally send via SMS.
    Returns (success, message, expires_in_seconds, otp).
    """
    key = f"{country_code}{phone}".replace(" ", "")
    otp = _generate_otp()
    expires_at = datetime.utcnow() + timedelta(seconds=OTP_EXPIRY_SECONDS)
    _otp_store[key] = (otp, expires_at)

    full_phone = f"{country_code} {phone}"
    sms_message = f"Your login OTP is {otp}. Valid for {OTP_EXPIRY_SECONDS // 60} minutes."
    sent = _send_sms(full_phone, sms_message)

    if sent:
        return True, "OTP sent successfully", OTP_EXPIRY_SECONDS, otp
    return False, "Failed to send OTP", 0, otp


def verify_otp(phone: str, otp: str, country_code: str = "+91") -> bool:
    """Verify OTP and invalidate it on success."""
    key = f"{country_code}{phone}".replace(" ", "")
    if key not in _otp_store:
        return False
    stored_otp, expires_at = _otp_store[key]
    if datetime.utcnow() > expires_at:
        del _otp_store[key]
        return False
    if stored_otp != otp:
        return False
    del _otp_store[key]
    return True
