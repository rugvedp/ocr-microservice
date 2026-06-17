from fastapi import APIRouter
from app.schemas import HealthResponse, StatusResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}


@router.get("/status", response_model=StatusResponse)
def status():
    try:
        import pytesseract
        version = str(pytesseract.get_tesseract_version())
        engine_status = "ready"
    except Exception:
        version = "unknown"
        engine_status = "unavailable"

    return {"engine": "tesseract", "status": engine_status, "version": version}
