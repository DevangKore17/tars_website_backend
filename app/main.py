from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import FRONTEND_URL
from app.routers.contact import router as contact_router
from app.core.exception_handlers import validation_exception_handler
from fastapi.exceptions import RequestValidationError

app = FastAPI(
    title="TARS Backend"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    contact_router
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)