import io
import time
import pytesseract
from PIL import Image


def run_ocr(image_bytes: bytes) -> dict:
    img = Image.open(io.BytesIO(image_bytes))

    start = time.perf_counter()
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

    blocks = []
    confidences = []
    for i, text in enumerate(data["text"]):
        text = text.strip()
        if not text:
            continue
        conf_raw = float(data["conf"][i])
        if conf_raw < 0:
            continue
        conf = round(conf_raw / 100.0, 4)
        x, y, w, h = (
            data["left"][i], data["top"][i],
            data["width"][i], data["height"][i],
        )
        blocks.append({
            "text": text,
            "confidence": conf,
            "bbox": [x, y, x + w, y + h],
        })
        confidences.append(conf)

    avg_conf = round(sum(confidences) / len(confidences), 4) if confidences else 0.0
    full_text = " ".join(b["text"] for b in blocks)

    return {
        "engine": "tesseract",
        "text": full_text,
        "confidence": avg_conf,
        "blocks": blocks,
        "processing_time_ms": elapsed_ms,
    }
