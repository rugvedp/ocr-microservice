from fastapi import APIRouter
from app.schemas import HealthResponse, StatusResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}


@router.get("/status", response_model=StatusResponse)
def status():
    try:
        from rapidocr_onnxruntime import RapidOCR  # noqa: F401
        import rapidocr_onnxruntime
        version = getattr(rapidocr_onnxruntime, "__version__", "unknown")
        engine_status = "ready"
    except Exception:
        version = "unknown"
        engine_status = "unavailable"

    return {"engine": "rapidocr", "status": engine_status, "version": version}
