# CropAI — Explainable, Uncertainty-Aware Agricultural Decision Support System

CropAI is a decoupled multi-service agricultural support platform. It implements three independent machine learning pipelines providing disease diagnosis, crop recommendation, and yield estimation with calibrated confidence limits and local explainability models.

---

## 1. System Architecture

CropAI uses a decoupled, service-oriented architecture keeping the front-end interface separated from the backend ML serving model container:

```text
    [ Streamlit Frontend UI (Port 8501) ] 
                     │
             HTTP (REST / JSON)
                     ▼
       [ FastAPI Serving API (Port 8000) ]
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
      [Disease]   [Crop]      [Yield]
      Services   Services    Services
         │           │           │
      [MobileNet] [Random]    [Random]
       (PyTorch)  (Forest)    (Forest)
         │           │           │
     [Grad-CAM]    [SHAP]      [SHAP]
     (Explanations) (Explanations) (Explanations)
         │           │           │
     [Entropy]  [Isotonic]   [Conformal]
    (Uncertainty) (Calibration) (Intervals)
```

---

## 2. Setup & Installation

### Prerequisite
- Python 3.12+
- Virtual Environment tool (`venv`)

### 1. Initialize Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 3. Dataset Setup

All datasets used by CropAI are documented in [data/README.md](file:///Users/bramhabajannavar/Desktop/Major%20project/data/README.md). To generate the synthetic datasets for local training:
```bash
python3 data/generate_datasets.py
```
This will populate `data/disease/`, `data/crop/`, and `data/yield/` with split partitions.

---

## 4. Training & Serialization

To train the models and export serialized binary checkpoints to the `artifacts/` folder:

```bash
# 1. Train Leaf Disease Classification Model (MobileNetV3 PyTorch)
python3 training/disease/train_disease.py

# 2. Train Crop Recommendation Classifier (Calibrated Random Forest)
python3 training/crop/train_crop.py

# 3. Train Crop Yield Regressor (Random Forest + Conformal Residuals)
python3 training/yield/train_yield.py
```

---

## 5. Running the Application

### Running the serving API (FastAPI)
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
The interactive Swagger API documentation will be available at: `http://localhost:8000/docs`.

### Running the User Interface (Streamlit)
```bash
streamlit run app/streamlit_app.py --server.port=8501
```
Access the dashboard at `http://localhost:8501`.

---

## 6. Docker Container Deployment

To launch the multi-container stack (FastAPI backend + Streamlit frontend):

```bash
docker-compose up --build
```
This command compiles the `Dockerfile` into separate communicating services on a bridge network.

---

## 7. Serving API Endpoints

### 1. Health Check
`GET /health`
- **Response:** `{"status": "ok", "models_loaded": {"disease": true, "crop": true, "yield": true}}`

### 2. Leaf Disease Diagnosis
`POST /api/v1/disease/predict` (Content-Type: `multipart/form-data`)
- **Payload:** `image=<binary_file>`
- **Response:**
  ```json
  {
    "prediction": "Tomato___Late_blight",
    "confidence": 0.94,
    "top_predictions": [{"class": "Tomato___Late_blight", "probability": 0.94}, ...],
    "uncertainty": {"entropy": 0.12, "reliability": "High", "method": "mc_dropout"},
    "explanation": {"explanation_available": true, "overlay_base64": "..."}
  }
  ```

### 3. Crop Recommendation
`POST /api/v1/crop/recommend` (Content-Type: `application/json`)
- **Payload:**
  ```json
  {
    "nitrogen": 80.0,
    "phosphorus": 45.0,
    "potassium": 40.0,
    "temperature": 25.0,
    "humidity": 80.0,
    "ph": 6.5,
    "rainfall": 120.0
  }
  ```
- **Response:**
  ```json
  {
    "recommended_crop": "Rice",
    "confidence": 0.87,
    "top_recommendations": [{"crop": "Rice", "probability": 0.87}, ...],
    "reliability": "High",
    "explanation": {"top_features": [{"feature": "rainfall", "value": 120.0, "shap_value": 0.31}, ...]}
  }
  ```

### 4. Yield Prediction
`POST /api/v1/yield/predict` (Content-Type: `application/json`)
- **Payload:**
  ```json
  {
    "crop": "Rice",
    "season": "Kharif",
    "rainfall": 1100.0,
    "temperature": 26.0,
    "area": 2.5,
    "confidence_level": 0.90
  }
  ```
- **Response:**
  ```json
  {
    "predicted_yield": 4.82,
    "unit": "tonnes/hectare",
    "interval": {"lower": 4.12, "upper": 5.54, "confidence_level": 0.90, "interval_width": 1.42},
    "explanation": {"top_features": [{"feature": "rainfall", "shap_value": 0.28}, ...]}
  }
  ```

---

## 8. Model Limitations & Disclaimers

- **Synthetic Training Scope:** Currently trained on generated datasets. Must be re-trained on actual PlantVillage/Kaggle dataset binaries before field use.
- **Grad-CAM Constraints:** CAM activation maps display spatial pixel correlation outputs, not clinical causal proof of leaf tissue diseases.
- **Decision Support Only:** CropAI outputs represent non-prescriptive recommendation bounds intended as professional decision support. Agronomic outcomes are not guaranteed.
