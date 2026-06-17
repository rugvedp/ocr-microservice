import io
from fastapi.testclient import TestClient
from PIL import Image, ImageDraw
from app.main import app

client = TestClient(app)


def _make_png(text: str = "Hello OCR") -> bytes:
    img = Image.new("RGB", (300, 80), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((10, 25), text, fill="black")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_ocr_response_structure():
    image_bytes = _make_png()
    response = client.post(
        "/ocr",
        files={"file": ("test.png", image_bytes, "image/png")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["engine"] == "rapidocr"
    assert isinstance(data["text"], str)
    assert 0.0 <= data["confidence"] <= 1.0
    assert isinstance(data["blocks"], list)
    assert isinstance(data["processing_time_ms"], float)


def test_ocr_block_structure():
    image_bytes = _make_png()
    response = client.post(
        "/ocr",
        files={"file": ("test.png", image_bytes, "image/png")},
    )
    data = response.json()
    for block in data["blocks"]:
        assert "text" in block
        assert "confidence" in block
        assert "bbox" in block
        assert len(block["bbox"]) == 4


def test_ocr_rejects_unsupported_type():
    response = client.post(
        "/ocr",
        files={"file": ("test.txt", b"not an image", "text/plain")},
    )
    assert response.status_code == 422
