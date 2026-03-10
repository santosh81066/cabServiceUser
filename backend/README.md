# Cab Service API – Backend

Python backend (FastAPI) for the Cab Service app. APIs are aligned with your **User (PAX)**, **Driver (DRV)**, and **Admin (ADM)** screens.

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- **API base:** http://localhost:8000  
- **Swagger UI:** http://localhost:8000/docs  
- **ReDoc:** http://localhost:8000/redoc  

**Deploy on cPanel (public hosting):** see **[DEPLOY.md](DEPLOY.md)** for pushing code safely and running the API on cPanel.

## Sending OTP to mobile (Python packages / providers)

There is **no single “send OTP” package**; you use an **SMS gateway** and call it from Python. Common options:

| Provider | Python usage | Region | Notes |
|----------|--------------|--------|--------|
| **Twilio** | `pip install twilio`, then `twilio.rest.Client` | Global | Simple API, free trial credits. |
| **MSG91** | No extra package (uses `urllib`), or `msg91-sms` on PyPI | India | Popular in India, OTP API. |
| **Fast2SMS** | `requests` to their REST API | India | Indian SMS API. |
| **AWS SNS** | `pip install boto3`, then `boto3.client('sns')` | Global | Good if you already use AWS. |
| **Nexmo (Vonage)** | `pip install vonage` | Global | REST API / SDK. |

This project **already supports Twilio and MSG91** in `app/services/otp_service.py`. If the right env vars are set, `/api/v1/auth/user/send-otp` will send real SMS.

**Twilio (global):**
```bash
pip install twilio
```
Set in `.env` or environment:
- `TWILIO_ACCOUNT_SID` – from Twilio console  
- `TWILIO_AUTH_TOKEN` – from Twilio console  
- `TWILIO_PHONE_NUMBER` – e.g. `+1234567890` (trial: only to verified numbers)

**MSG91 (India, no extra package):**
- Sign up at [msg91.com](https://msg91.com), get an auth key.
- Set `MSG91_AUTH_KEY` in env.

If **none** of these are set, the API still generates and stores OTP but only logs the message (no SMS). Use `DEBUG=true` to get the OTP in the API response for testing.

## Firebase OTP (recommended)

Use **Firebase Phone Authentication** so Firebase sends the OTP; your app only verifies the token with this backend.

**Flow:**
1. **App (client)** uses Firebase Client SDK: request OTP with phone number → Firebase sends SMS.
2. User enters OTP in the app.
3. **App** confirms OTP with Firebase → receives Firebase **ID token**.
4. **App** calls this backend with that token:  
   `POST /api/v1/auth/user/firebase-login` or `POST /api/v1/auth/driver/firebase-login`  
   Body: `{ "id_token": "<firebase_id_token>" }`.
5. **Backend** verifies the token with Firebase Admin SDK and returns your `access_token` and `user_id`.

**Backend setup:**
1. In [Firebase Console](https://console.firebase.google.com): enable **Phone** sign-in, get **Project ID** (e.g. `cabservice-6c9ff`).
2. Project settings → Service accounts → **Generate new private key** → save the JSON file.
3. **Where to keep the JSON:** put it in the **`backend`** folder. Name it e.g. `firebase-service-account.json`.  
   **Do not commit this file** (it’s in `.gitignore`).
4. Create `backend/.env` from `backend/.env.example` and set:
   - `FIREBASE_PROJECT_ID` = your Firebase project ID (e.g. `cabservice-6c9ff`)
   - `GOOGLE_APPLICATION_CREDENTIALS` = path to that JSON. From the `backend` folder use: `./firebase-service-account.json`

`firebase-admin` is already in `requirements.txt`. No Twilio/MSG91 needed when using Firebase OTP.

## What happens when a new user logs in (Firebase OTP)

1. **In the app:** User enters phone number → your app calls **Firebase Client SDK** (e.g. `signInWithPhoneNumber`) → Firebase sends OTP via SMS → user enters OTP → app calls `confirmationResult.confirm(otp)` → Firebase creates the user (first time) and returns an ID token.
2. **App** sends that ID token to your backend:  
   `POST /api/v1/auth/user/firebase-login` with `{ "id_token": "..." }`.
3. **Backend** verifies the token with Firebase, then:
   - Returns `access_token`, `user_id`, `role` (same for new and existing users).
   - Sets **`is_new_user`** in the response: **`true`** the first time this Firebase UID logs in, **`false`** on later logins.
4. **Your app** can use `is_new_user` to show onboarding or “Complete your profile” for first-time users, and go straight to home for returning users.

Right now the backend does **not** store user profiles in a database; endpoints like `GET /users/me` return stub data. To persist name, email, etc., add a DB and create/update a user record on login (e.g. when `is_new_user` is true, create the record).

## Free & open-source: sending SMS

Real SMS has to go through the telecom network, so there is no 100% free solution without any cost. These are the **free-software** options:

| Option | Cost | Open source | Notes |
|--------|------|-------------|--------|
| **Gammu + GSM modem** | Modem + SIM (one-time + mobile plan) | ✅ Yes | Use a USB GSM modem/dongle and a SIM card. Software is free ([Gammu](https://wammu.eu/), [python-gammu](https://pypi.org/project/python-gammu/)). This project can use it if `GAMMU_DEVICE` is set. |
| **Kannel / Kamex** | Same as above (modem + SIM) or SMPP | ✅ Yes | [Kannel](https://www.kannel.org/) / [Kamex](https://github.com/vaska94/kamex) – gateway that can use a modem or SMPP. |
| **Free tiers** | $0 for limited use | ❌ No | Twilio trial, MSG91 free tier – not open source but no cost for small usage. |
| **Email-to-SMS** | Free | N/A | Some carriers accept email (e.g. `number@carrier.com`). Unreliable, carrier-specific, often delayed or blocked. |

**Using Gammu (USB GSM modem + SIM) with this project**

1. Get a USB GSM modem (e.g. Huawei E3131, ZTE MF190) and a SIM with SMS balance.
2. Install Gammu and python-gammu on the server (e.g. `apt install gammu` then `pip install python-gammu`).
3. Configure Gammu for your device (e.g. `gammu-config` or set `GAMMU_DEVICE` to the modem’s serial port).
4. Set in env: `GAMMU_DEVICE=/dev/ttyUSB0` (or your modem’s device). The app will then send OTP via Gammu when available.

No cloud API key needed; all traffic goes through your SIM. You only pay for the SIM’s SMS pack.

## API overview (by screen layer)

### Auth
| Screen | Method | Endpoint |
|--------|--------|----------|
| PAX_01 Login | POST | `/api/v1/auth/user/send-otp` |
| PAX_02 Verify OTP | POST | `/api/v1/auth/user/verify-otp` |
| **Firebase OTP** | POST | `/api/v1/auth/user/firebase-login` |
| DRV_01 Driver Login | POST | `/api/v1/auth/driver/send-otp` |
| DRV_02 OTP Verify | POST | `/api/v1/auth/driver/verify-otp` |
| **Firebase OTP (driver)** | POST | `/api/v1/auth/driver/firebase-login` |
| ADM_01 Admin Login | POST | `/api/v1/auth/admin/login` |
| PAX_26 Logout | POST | `/api/v1/auth/logout` |

### User (Passenger)
| Screen | Method | Endpoint |
|--------|--------|----------|
| PAX_14 My Profile | GET | `/api/v1/users/me` |
| PAX_11 Edit Profile | PATCH | `/api/v1/users/me` |
| PAX_16 Wallet | GET | `/api/v1/users/wallet` |
| PAX_17 Add Money | POST | `/api/v1/users/wallet/add-money` |
| PAX_24 Saved Places | GET/POST | `/api/v1/users/saved-places` |
| PAX_18 Apply Coupon | POST | `/api/v1/users/coupons/apply` |
| PAX_19 Refer & Earn | GET | `/api/v1/users/referral` |
| PAX_25 Notifications | GET/PUT | `/api/v1/users/notifications/preferences` |
| PAX_13 Discount History | GET | `/api/v1/users/discounts/history` |
| PAX_20 Reward Progress | GET | `/api/v1/users/rewards/progress` |

### Rides
| Screen | Method | Endpoint |
|--------|--------|----------|
| PAX_03/04/05 Book | POST | `/api/v1/rides/book` |
| Fare estimate | POST | `/api/v1/rides/fare-estimate` |
| PAX_10 Ride History | GET | `/api/v1/rides/history` |
| PAX_12 Ride Detail | GET | `/api/v1/rides/{trip_id}` |
| PAX_06 Driver Assigned | GET | `/api/v1/rides/{trip_id}/driver` |
| PAX_07 Live Trip | GET | `/api/v1/rides/{trip_id}/live` |
| PAX_08 Payment | GET/POST | `/api/v1/rides/{trip_id}/payment-methods`, `.../pay` |
| PAX_09 Rate Driver | POST | `/api/v1/rides/{trip_id}/rate` |
| Cancel ride | POST | `/api/v1/rides/{trip_id}/cancel` |

### Support
| Screen | Method | Endpoint |
|--------|--------|----------|
| PAX_21 Help & Support | GET | `/api/v1/support/categories` |
| PAX_22 Support Ticket | POST | `/api/v1/support/tickets` |
| Track ticket | GET | `/api/v1/support/tickets`, `.../tickets/{id}` |

### Driver
| Screen | Method | Endpoint |
|--------|--------|----------|
| DRV_03 KYC status | GET | `/api/v1/drivers/kyc/status` |
| DRV_03A–E KYC steps | POST | `/api/v1/drivers/kyc/aadhaar`, `.../driving-license`, `.../rc`, `.../insurance`, `.../bank` |
| DRV_03F Submit KYC | POST | `/api/v1/drivers/kyc/submit` |
| DRV_04 Service Setup | PUT | `/api/v1/drivers/service-setup` |
| DRV_05 Home | GET | `/api/v1/drivers/home` |
| DRV_06/07/08 Requests | GET/POST | `/api/v1/drivers/requests/pending`, `.../respond` |
| DRV_10–14 Trip flow | POST | `/api/v1/drivers/trips/{id}/arrived`, `.../start`, `.../complete`, `.../payment-collected` |
| DRV_15 Earnings | GET | `/api/v1/drivers/earnings` |
| DRV_16 Payout | POST | `/api/v1/drivers/payout` |
| DRV_17 Incentives | GET | `/api/v1/drivers/incentives` |
| DRV_18 Ride History | GET | `/api/v1/drivers/rides/history` |
| DRV_19 Ratings | GET | `/api/v1/drivers/ratings` |
| DRV_21/22 Profile & Settings | GET/PUT | `/api/v1/drivers/profile`, `.../settings` |
| Go online/offline | POST | `/api/v1/drivers/go-online`, `.../go-offline` |

### Admin
| Screen | Method | Endpoint |
|--------|--------|----------|
| ADM_03 Dashboard | GET | `/api/v1/admin/dashboard` |
| ADM_04 Live Trips | GET | `/api/v1/admin/live-trips` |
| ADM_05 KYC Queue | GET/POST | `/api/v1/admin/kyc/queue`, `.../action` |
| ADM_06 Fleet Compliance | GET/POST | `/api/v1/admin/fleet/compliance`, `.../sweep` |
| ADM_06A/06B Vehicles | GET/POST/PUT | `/api/v1/admin/vehicles`, `.../pricing` |
| ADM_07 Pricing | GET/PUT | `/api/v1/admin/pricing` |
| ADM_08 Loyalty | GET/PUT | `/api/v1/admin/loyalty` |
| ADM_09 Allocation | GET/POST | `/api/v1/admin/allocation`, `.../apply` |
| ADM_10 Payout | GET/POST | `/api/v1/admin/payout/stats`, `.../release`, `.../retry-failed` |
| ADM_11 Disputes | GET/POST | `/api/v1/admin/disputes`, `.../action` |
| ADM_12 Reports | GET | `/api/v1/admin/reports/stats`, `.../city-revenue` |

## Auth

- **User / Driver:** Send OTP → verify OTP → use returned `access_token` in header:  
  `Authorization: Bearer <access_token>`
- **Admin:** Login with email + password → use returned `access_token` in the same way.

Protected routes expect `Authorization: Bearer <token>` (any non-empty token is accepted for now).

## Request body examples (JSON)

Use these as the **JSON body** for POST/PUT/PATCH requests. Replace placeholders with your values.

### Auth

**POST `/api/v1/auth/user/send-otp`** (same for driver: `/auth/driver/send-otp`)
```json
{
  "phone": "9899999921",
  "country_code": "+91",
  "referral_code": "PROMO10"
}
```
`referral_code` is optional.

**Does it send real SMS?** The API generates and stores a 6-digit OTP (valid 3 min). Real SMS is sent only after you add an SMS provider in `app/services/otp_service.py` (e.g. MSG91, Twilio). For local testing: run with `DEBUG=true` so the response includes `otp`, or check server logs where the OTP is printed.

**POST `/api/v1/auth/user/verify-otp`** (same for driver)
```json
{
  "phone": "9899999921",
  "country_code": "+91",
  "otp": "123456"
}
```
`otp` must be 6 digits.

**POST `/api/v1/auth/admin/login`**
```json
{
  "email": "admin@cabops.com",
  "password": "your_password"
}
```

**POST `/api/v1/auth/user/firebase-login`** (same body for **driver**: `/api/v1/auth/driver/firebase-login`)  
Use this when you use **Firebase Phone Auth**: after the user completes OTP in the app, send the Firebase ID token here.
```json
{
  "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6..."
}
```
Backend verifies the token with Firebase and returns `access_token`, `user_id`, `role`, and `is_new_user` (true on first login).

### User (passenger)

**PATCH `/api/v1/users/me`** (edit profile) — all fields optional
```json
{
  "name": "Santosh Kumar",
  "email": "santosh@mail.com",
  "gender": "Male",
  "preferred_language": "English"
}
```

**POST `/api/v1/users/wallet/add-money`**
```json
{
  "amount_inr": 500,
  "payment_method": "upi"
}
```
`payment_method`: `"upi"` | `"card"` | `"wallet"` | `"cash"`

**POST `/api/v1/users/saved-places`**
```json
{
  "label": "Home",
  "address": "HSR Layout, Bengaluru"
}
```

**POST `/api/v1/users/coupons/apply`**
```json
{
  "coupon_code": "WELCOME10",
  "trip_id": "TRP-88231"
}
```
`trip_id` optional.

**PUT `/api/v1/users/notifications/preferences`**
```json
{
  "trip_alerts": true,
  "promo_offers": true,
  "outstation_deals": false,
  "payment_reminders": true,
  "sms_notifications": true
}
```

### Rides

**POST `/api/v1/rides/fare-estimate`** and **POST `/api/v1/rides/book`**

Single ride:
```json
{
  "ride_type": "single",
  "pickup": { "latitude": 12.935, "longitude": 77.624, "address": "Koramangala, Bengaluru" },
  "drop": { "latitude": 13.199, "longitude": 77.707, "address": "Airport, Bengaluru" },
  "vehicle_type": "mini"
}
```

Sharing (add to above): `"seats": 2, "max_detour_mins": 5, "gender_pref": "any"`  
Outstation (add): `"from_city": "Bengaluru", "to_city": "Mysuru", "departure_date": "2026-03-12", "departure_time": "07:30", "trip_type": "one_way", "luggage": "medium"`  
`ride_type`: `"single"` | `"sharing"` | `"outstation"`. `gender_pref`: `"any"` | `"female_only"` | `"male_only"`.

**POST `/api/v1/rides/{trip_id}/pay`**
```json
{
  "trip_id": "TRP-88231",
  "method": "upi",
  "amount_inr": 280,
  "upi_id": "santosh@upi"
}
```
`upi_id` optional when method is UPI.

**POST `/api/v1/rides/{trip_id}/rate`**
```json
{
  "trip_id": "TRP-88231",
  "rating": 5,
  "comment": "Smooth ride."
}
```
`rating` 1–5; `comment` optional.

### Support

**POST `/api/v1/support/tickets`**
```json
{
  "trip_id": "TRP-88231",
  "issue_type": "payment_refund",
  "description": "Fare was higher than estimated.",
  "attachment_url": "https://example.com/screenshot.png"
}
```
`trip_id` and `attachment_url` optional. `issue_type`: e.g. `trip_issues` | `payment_refund` | `account_profile` | `safety` | `outstation`

### Driver

**PUT `/api/v1/drivers/service-setup`**
```json
{
  "vehicle_id": "v_swift_001",
  "active_categories": ["single", "sharing", "outstation"],
  "sharing_pref": "any",
  "max_seats": 3,
  "luggage": "medium"
}
```
`sharing_pref`: `"any"` | `"female_only"` | `"male_only"`

**POST `/api/v1/drivers/requests/respond`**
```json
{
  "request_id": "req_001",
  "accept": true
}
```

**POST `/api/v1/drivers/trips/start`**
```json
{
  "trip_id": "TRP-88231",
  "otp": "6421"
}
```

**POST `/api/v1/drivers/payout`**
```json
{
  "amount_inr": 3000
}
```

**PUT `/api/v1/drivers/settings`** — all optional
```json
{
  "online_auto_accept": false,
  "outstation_requests": true,
  "sharing_requests": true,
  "night_shift_mode": false,
  "language": "en",
  "notification_sounds": true
}
```

**KYC (POST each):**  
`/kyc/aadhaar`: `{"aadhaar_number":"123456789012","full_name":"Ravi Kumar","date_of_birth":"1990-05-15","otp":"123456"}`  
`/kyc/driving-license`: `{"dl_number":"KA0120190123456","issue_date":"2019-01-10","expiry_date":"2029-01-10","dl_front_url":"https://...","dl_back_url":"https://..."}`  
`/kyc/rc`: `{"vehicle_number":"KA01AB1234","owner_name":"Ravi Kumar","rc_front_url":"https://...","rc_back_url":"https://..."}`  
`/kyc/insurance`: `{"policy_number":"POL123456","provider":"HDFC Ergo","expiry_date":"2026-12-31","document_url":"https://..."}`  
`/kyc/bank`: `{"account_holder_name":"Ravi Kumar","account_number":"123456789012","ifsc_code":"HDFC0001234","upi_id":"ravi@upi","cheque_url":"https://..."}`

### Admin

**POST `/api/v1/admin/kyc/action`**
```json
{
  "driver_id": "DRV-9832",
  "action": "approve",
  "reason": "Documents verified"
}
```
`action`: `"approve"` | `"reject"` | `"hold"`

**POST `/api/v1/admin/vehicles`**
```json
{
  "vehicle_name": "Mini",
  "vehicle_type": "single",
  "base_fare_inr": 40,
  "per_km_inr": 12,
  "per_min_inr": 2
}
```

**PUT `/api/v1/admin/vehicles/pricing`**
```json
{
  "vehicle_id": "v_mini",
  "base_fare_inr": 40,
  "per_km_inr": 12
}
```

**PUT `/api/v1/admin/pricing`**
```json
{
  "commission_percent": 22,
  "base_fare_index": 1.0,
  "max_surge": 2.5,
  "surge_zones_active": 7,
  "city": "Bengaluru"
}
```

**PUT `/api/v1/admin/loyalty`**
```json
{
  "tiers": [
    {"ride_number": 1, "discount_percent": 10},
    {"ride_number": 2, "discount_percent": 20},
    {"ride_number": 4, "discount_percent": 25},
    {"ride_number": 8, "discount_percent": 30},
    {"ride_number": 16, "discount_percent": 40}
  ],
  "cap_per_user_per_day_inr": 80,
  "segments": ["new", "frequent", "outstation"]
}
```

**POST `/api/v1/admin/disputes/action`**
```json
{
  "dispute_id": "d1",
  "action": "approve_refund",
  "reason": "Fare mismatch confirmed"
}
```
`action`: `"approve_refund"` | `"reject"` | `"escalate"`

---

## Next steps

- Add a real database (e.g. PostgreSQL + SQLAlchemy) and wire models.
- Integrate SMS/OTP provider for send/verify OTP.
- Add JWT creation/validation for tokens.
- Add file upload for KYC documents (e.g. S3 or local storage).
