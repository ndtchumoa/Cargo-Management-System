"""
Cargo Management System — FastAPI Backend
Entry point: uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import check_connection
from app.routers import orders, invoices, assignments, analytics, optimize

# ── App instance ─────────────────────────────

app = FastAPI(
    title       = "Cargo Management System API",
    description = "REST API cho hệ thống quản lý vận chuyển hàng hóa cargo_db",
    version     = "1.0.0",
    docs_url    = "/docs",
    redoc_url   = "/redoc",
)

# ── CORS ─────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins     = settings.origins_list,
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

# ── Routers ──────────────────────────────────

app.include_router(orders.router)
app.include_router(invoices.router)
app.include_router(assignments.router)
app.include_router(analytics.router)
app.include_router(optimize.router)

# ── Startup / Health ─────────────────────────

@app.on_event("startup")
async def startup_event():
    ok = check_connection()
    status = "✅ Kết nối thành công" if ok else "❌ Không thể kết nối"
    print(f"[DB] {status} → {settings.DB_NAME}@{settings.DB_HOST}:{settings.DB_PORT}")


@app.get("/", tags=["Health"])
def root():
    return {
        "app":     "Cargo Management System",
        "version": "1.0.0",
        "status":  "running",
        "docs":    "/docs",
    }


@app.get("/health", tags=["Health"])
def health():
    db_ok = check_connection()
    return {
        "api": "ok",
        "database": "ok" if db_ok else "error",
    }
