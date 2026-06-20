"""
TARS Contact Form Backend — Application Settings

Centralized configuration loaded from environment variables / .env file.
Uses pydantic-settings for type-safe, validated configuration.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ───────────────────────────────────────────
    APP_NAME: str = "TARS Contact Backend"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    ALLOWED_ORIGINS: str = "*"  # comma-separated

    # ── Email Recipient ───────────────────────────────────────
    RECEIVER_EMAIL: str = ""  # who receives contact form submissions

    # ── SMTP Configuration ────────────────────────────────────
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_USE_TLS: bool = True

    @property
    def cors_origins(self) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    @property
    def smtp_sender(self) -> str:
        """Return the SMTP username as the sender address."""
        return self.SMTP_USERNAME

    @property
    def receiver(self) -> str:
        """Return the receiver, falling back to SMTP username."""
        return self.RECEIVER_EMAIL or self.SMTP_USERNAME


# Singleton — import this everywhere
settings = Settings()
