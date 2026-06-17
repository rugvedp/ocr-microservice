from pydantic import BaseModel
from typing import List


class HealthResponse(BaseModel):
    status: str


class StatusResponse(BaseModel):
    engine: str
    status: str
    version: str


class Block(BaseModel):
    text: str
    confidence: float
    bbox: List[int]


class OCRResponse(BaseModel):
    engine: str
    text: str
    confidence: float
    blocks: List[Block]
    processing_time_ms: float
