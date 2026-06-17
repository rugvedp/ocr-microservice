from fastapi import FastAPI
from app.routers import health, ocr

app = FastAPI(title="Tesseract OCR Service", version="1.0.0")
app.include_router(health.router)
app.include_router(ocr.router)
