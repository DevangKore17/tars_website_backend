"""
TARS Contact Form Backend — FastAPI Application Entry Point

Initializes the app, middleware, routes, and lifespan events.
Run with:  uvicorn app.main:app --reload --port 8000
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.routes.contact import router as contact_router
from app.utils.logging import setup_logging, get_logger


# ── Set up logging before anything else ───────────────────────
setup_logging()
logger = get_logger("main")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Lifespan — startup / shutdown hooks
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: runs on startup and shutdown."""
    logger.info("[START] %s starting up...", settings.APP_NAME)
    logger.info("   Debug mode : %s", settings.DEBUG)
    logger.info("   Log level  : %s", settings.LOG_LEVEL)
    logger.info("   SMTP host  : %s:%d", settings.SMTP_HOST, settings.SMTP_PORT)

    yield  # ← app is running

    logger.info("[STOP] %s shutting down...", settings.APP_NAME)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  FastAPI app
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description=(
        "Contact form backend for the TARS website. "
        "Receives form submissions and sends email notifications via SMTP."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ── CORS middleware ───────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Custom validation exception handler ──────────────────────
# Returns clean, frontend-friendly error messages on 422

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    errors = []
    for err in exc.errors():
        errors.append({
            "field": err["loc"][-1],
            "message": err["msg"],
        })
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "errors": errors,
        },
    )


# ── Register routes ──────────────────────────────────────────
app.include_router(contact_router)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Health check
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.get(
    "/health",
    tags=["System"],
    summary="Health check",
    description="Returns a simple health status for uptime monitors.",
)
async def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": "1.0.0",
    }


@app.get(
    "/",
    tags=["System"],
    summary="Root",
    include_in_schema=False,
)
async def root():
    return {
        "service": settings.APP_NAME,
        "docs": "/docs",
        "health": "/health",
    }
