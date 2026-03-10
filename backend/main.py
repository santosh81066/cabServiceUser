"""
Cab Service API - Backend
User (PAX), Driver (DRV), and Admin (ADM) flows aligned with screens.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, users, rides, support, drivers, admin

app = FastAPI(
    title=settings.app_name,
    description="APIs for Cab Service: User ride booking, Driver KYC/trips/earnings, Admin operations.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prefix = settings.api_prefix

app.include_router(auth.router, prefix=prefix)
app.include_router(users.router, prefix=prefix)
app.include_router(rides.router, prefix=prefix)
app.include_router(support.router, prefix=prefix)
app.include_router(drivers.router, prefix=prefix)
app.include_router(admin.router, prefix=prefix)


@app.get("/")
def root():
    return {
        "app": settings.app_name,
        "docs": "/docs",
        "redoc": "/redoc",
        "api_prefix": prefix,
    }


@app.get("/health")
def health():
    return {"status": "ok"}
