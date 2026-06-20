"""
TARS Contact Form Backend — Pydantic Models

Data models for the contact form submission endpoint.
Validates incoming form data strictly with Pydantic.
"""

from pydantic import BaseModel, EmailStr, Field


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Contact form request
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ContactRequest(BaseModel):
    """Validated contact form submission from the frontend."""

    name: str = Field(
        ..., min_length=2, max_length=100,
        description="Sender's full name",
    )
    email: EmailStr = Field(
        ..., description="Sender's email address (RFC 5322)",
    )
    message: str = Field(
        ..., min_length=10, max_length=5000,
        description="Message body from the contact form",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Response models
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ContactResponse(BaseModel):
    """Response returned after accepting a contact form submission."""

    success: bool = True
    message: str = "Request accepted for processing"


class ErrorResponse(BaseModel):
    """Standardized error response body."""

    success: bool = False
    detail: str
