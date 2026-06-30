"""
Cargo Management System — FastAPI Backend
Entry point: uvicorn app.main:app --reload
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import check_connection
from app.routers import orders, invoices, assignments, analytics, optimize


# ── Lifespan (thay cho on_event đã deprecated) ─

@asynccontextmanager
async def lifespan(app: FastAPI):
    ok = check_connection()
    status = "✅ Kết nối thành công" if ok else "❌ Không thể kết nối"
    print(f"[DB] {status} → {settings.DB_NAME}@{settings.DB_HOST}:{settings.DB_PORT}")
    yield
    # (Không cần dọn dẹp gì khi shutdown)


# ── App instance ─────────────────────────────

app = FastAPI(
    title       = "Cargo Management System API",
    description = "REST API cho hệ thống quản lý vận chuyển hàng hóa cargo_db",
    version     = "1.0.0",
    docs_url    = "/docs",
    redoc_url   = "/redoc",
    lifespan    = lifespan,
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

# ── Health ───────────────────────────────────

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
