from fastapi import (
    APIRouter,
    BackgroundTasks,
    status
)

from app.schemas.contact import ContactRequest
from app.services.email_service import send_contact_email

router = APIRouter(
    prefix="/api/contact",
    tags=["Contact"]
)


@router.post(
    "/",
    status_code=status.HTTP_202_ACCEPTED
)
async def contact(
    data: ContactRequest,
    background_tasks: BackgroundTasks
):

    background_tasks.add_task(
        send_contact_email,
        data.name,
        data.email,
        data.message
    )

    return {
        "success": True,
        "message": "Request accepted for processing"
    }