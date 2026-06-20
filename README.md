# TARS Contact Form Backend

Contact form backend for the TARS website. Receives form submissions from the frontend, validates them with Pydantic, and sends email notifications via SMTP in the background.

## Architecture

```
Frontend → POST /api/contact → Validate (Pydantic) → 202 Accepted
                                       ↓
                                BackgroundTask
                                       ↓
                             Send Email via SMTP
```

**Key design principles:**
- **Reply instantly** — returns 202 before any processing
- **Validate strictly** — Pydantic rejects malformed payloads at the gate
- **Process in background** — SMTP send never blocks the response

## Quick Start

```bash
# 1. Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
copy .env.example .env
# Edit .env with your SMTP credentials

# 4. Run the server
uvicorn app.main:app --reload --port 8000

# 5. Open the docs
# http://localhost:8000/docs
```

## API Endpoints

| Method | Path             | Description                        | Auth |
|--------|------------------|------------------------------------|------|
| POST   | `/api/contact`   | Submit a contact form              | None |
| GET    | `/health`        | Health check                       | None |
| GET    | `/docs`          | Interactive Swagger UI             | None |

## Configuration

All settings are loaded from environment variables (or `.env` file):

| Variable           | Default                | Description                       |
|--------------------|------------------------|-----------------------------------|
| `LOG_LEVEL`        | `INFO`                 | Logging level                     |
| `DEBUG`            | `false`                | Enable debug mode                 |
| `ALLOWED_ORIGINS`  | `*`                    | CORS allowed origins (comma-separated) |
| `APP_NAME`         | `TARS Contact Backend` | Application name (logs & metadata) |
| `RECEIVER_EMAIL`   | _(empty)_              | Who receives contact form emails  |
| `SMTP_HOST`        | `smtp.gmail.com`       | SMTP server hostname              |
| `SMTP_PORT`        | `587`                  | SMTP server port                  |
| `SMTP_USERNAME`    | _(empty)_              | SMTP login username               |
| `SMTP_PASSWORD`    | _(empty)_              | SMTP login password               |
| `SMTP_USE_TLS`     | `true`                 | Enable STARTTLS                   |

## Frontend Integration

The frontend (React + Vite) sends a `POST /api/contact` request with:

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "message": "Hello from the contact form!"
}
```

**Development:** Vite's dev proxy forwards `/api/*` → `http://localhost:8000` automatically.

**Production:** Set `VITE_API_URL` in the frontend to your deployed backend URL.

## Testing

```bash
# Run all tests
pytest tests/ -v

# Test with curl
curl -X POST http://localhost:8000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "message": "Hello from the contact form!"
  }'
```

Expected response (`202 Accepted`):
```json
{
  "success": true,
  "message": "Request accepted for processing"
}
```

## Project Structure

```
tars backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Settings (pydantic-settings)
│   ├── models/
│   │   └── email.py         # Pydantic request/response models
│   ├── routes/
│   │   └── contact.py       # POST /api/contact endpoint
│   ├── services/
│   │   └── email_service.py # Background SMTP email sending
│   └── utils/
│       └── logging.py       # Structured logging
├── tests/
│   └── __init__.py
├── requirements.txt
├── .env.example
└── README.md
```
