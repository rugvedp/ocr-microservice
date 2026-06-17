import time
import numpy as np
import cv2
from rapidocr_onnxruntime import RapidOCR

_engine: RapidOCR | None = None


def get_engine() -> RapidOCR:
    global _engine
    if _engine is None:
        _engine = RapidOCR()
    return _engine


def run_ocr(image_bytes: bytes) -> dict:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image bytes")

    engine = get_engine()
    start = time.perf_counter()
    result, _ = engine(img)
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

    if not result:
        return {
            "engine": "rapidocr",
            "text": "",
            "confidence": 0.0,
            "blocks": [],
            "processing_time_ms": elapsed_ms,
        }

    blocks = []
    confidences = []
    for bbox_points, text, conf in result:
        xs = [int(p[0]) for p in bbox_points]
        ys = [int(p[1]) for p in bbox_points]
        blocks.append({
            "text": text,
            "confidence": round(float(conf), 4),
            "bbox": [min(xs), min(ys), max(xs), max(ys)],
        })
        confidences.append(float(conf))

    avg_conf = round(sum(confidences) / len(confidences), 4)
    full_text = "\n".join(b["text"] for b in blocks)

    return {
        "engine": "rapidocr",
        "text": full_text,
        "confidence": avg_conf,
        "blocks": blocks,
        "processing_time_ms": elapsed_ms,
    }
