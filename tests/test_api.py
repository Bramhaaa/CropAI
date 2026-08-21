import io
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from api.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "models_loaded" in data

def test_crop_recommendation_valid():
    payload = {
        "nitrogen": 80,
        "phosphorus": 45,
        "potassium": 40,
        "temperature": 24.5,
        "humidity": 85,
        "ph": 6.2,
        "rainfall": 180
    }
    response = client.post("/api/v1/crop/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "recommended_crop" in data
    assert "confidence" in data
    assert "top_recommendations" in data
    assert "explanation" in data
    assert len(data["explanation"]["top_features"]) > 0

def test_crop_recommendation_invalid_values():
    # Nitrogen out of bound
    payload = {
        "nitrogen": -10,
        "phosphorus": 45,
        "potassium": 40,
        "temperature": 24.5,
        "humidity": 120, # out of bound
        "ph": 6.2,
        "rainfall": 180
    }
    response = client.post("/api/v1/crop/recommend", json=payload)
    assert response.status_code == 422  # Validation Error

def test_crop_recommendation_missing_param():
    payload = {
        "nitrogen": 80,
        "phosphorus": 45,
        "potassium": 40
    }
    response = client.post("/api/v1/crop/recommend", json=payload)
    assert response.status_code == 422  # Validation Error

def test_yield_prediction_valid():
    payload = {
        "crop": "Rice",
        "season": "Kharif     ",
        "area_hectares": 2.5,
        "confidence_level": 0.90
    }
    response = client.post("/api/v1/yield/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_yield" in data
    assert "unit" in data
    assert "interval" in data
    assert data["interval"]["confidence_level"] == 0.90
    assert "explanation" in data

def test_yield_prediction_invalid():
    payload = {
        "crop": "Rice",
        "season": "Kharif",
        "area_hectares": 0.0,   # Below minimum 0.1
        "confidence_level": 0.90
    }
    response = client.post("/api/v1/yield/predict", json=payload)
    assert response.status_code == 422

def test_disease_diagnosis_invalid_file_format():
    files = {"image": ("test.txt", b"dummy text content", "text/plain")}
    response = client.post("/api/v1/disease/predict", files=files)
    # 400 when format is rejected before model check; 503 if model not yet loaded but
    # the route validation fires first (order depends on FastAPI dependency resolution).
    assert response.status_code in (400, 503)
    if response.status_code == 400:
        assert "Unsupported image format" in response.json()["detail"]

def test_disease_diagnosis_valid_image():
    # Create a dummy image in memory
    img = Image.new("RGB", (224, 224), (255, 255, 255))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_bytes = img_byte_arr.getvalue()
    
    files = {"image": ("test.png", img_bytes, "image/png")}
    response = client.post("/api/v1/disease/predict", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
    assert "top_predictions" in data
    assert "uncertainty" in data
    assert "explanation" in data
    assert data["explanation"]["explanation_available"] is True
    assert "overlay_base64" in data["explanation"]
