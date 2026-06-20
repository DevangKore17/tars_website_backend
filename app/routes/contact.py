"""
TARS Contact Form Backend — Contact Form Route

Receives contact form submissions from the frontend,
validates the data, and queues a background email send.
Returns 202 Accepted immediately — fast response.
"""

from fastapi import APIRouter, BackgroundTasks, status

from app.models.email import ContactRequest, ContactResponse
from app.services.email_service import send_contact_email
from app.utils.logging import get_logger

logger = get_logger("contact")

router = APIRouter(prefix="/api/contact", tags=["Contact"])


@router.post(
    "",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ContactResponse,
    summary="Submit a contact form",
    description=(
        "Accepts a contact form submission (name, email, message), "
        "validates it with Pydantic, and sends an email notification "
        "in the background. Returns 202 Accepted immediately."
    ),
)
async def submit_contact_form(
    data: ContactRequest,
    background_tasks: BackgroundTasks,
) -> ContactResponse:
    """
    Contact form submission endpoint.

    Flow:
      1. Pydantic auto-validates the body (422 if malformed)
      2. Queue background email send
      3. Return 202 Accepted — FAST
    """

    logger.info(
        "[OK] Contact form received from %s (%s) - queued for email",
        data.name,
        data.email,
    )

    background_tasks.add_task(
        send_contact_email,
        data.name,
        data.email,
        data.message,
    )

    return ContactResponse(
        success=True,
        message="Request accepted for processing",
    )
