from fastapi import APIRouter, File, HTTPException, UploadFile
from app.schemas import OCRResponse
from app.engine import run_ocr

router = APIRouter()

_SUPPORTED = {
    "image/jpeg", "image/png", "image/tiff",
    "image/bmp", "image/webp",
}


@router.post("/ocr", response_model=OCRResponse)
async def ocr(file: UploadFile = File(...)):
    if file.content_type not in _SUPPORTED:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported file type: {file.content_type}. "
                   f"Accepted: {sorted(_SUPPORTED)}",
        )
    image_bytes = await file.read()
    try:
        result = run_ocr(image_bytes)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"OCR engine error: {exc}")
    return result
