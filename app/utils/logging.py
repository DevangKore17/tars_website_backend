"""
TARS Contact Form Backend — Structured Logging

Sets up structured logging with consistent formatting across all modules.
Each component gets its own named logger for clean filtering.
"""

import logging
import sys
from app.config import settings


def setup_logging() -> None:
    """Configure root logger with structured format and appropriate level."""

    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # ── Formatter ─────────────────────────────────────────────
    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ── Console Handler ───────────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    # ── Root Logger ───────────────────────────────────────────
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove any existing handlers to avoid duplicates on reload
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)

    # Quiet down noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a named logger for a specific component.

    Usage:
        from app.utils.logging import get_logger
        logger = get_logger("contact")
        logger.info("Form received", extra={"name": "Jane"})
    """
    return logging.getLogger(f"tars.{name}")
