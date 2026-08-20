# CropAI — Architecture Documentation

## Overall Architecture
CropAI is designed around a decoupled, service-oriented architecture with a clear separation of concerns between training, inference serving, and the user interface. The frontend (Streamlit) acts strictly as a presentation layer communicating via HTTP requests with the backend API (FastAPI), which in turn calls dedicated modular ML services.

```text
  [ Streamlit UI ]  <--- HTTP (JSON / Multipart) --->  [ FastAPI Serving Layer ]
                                                                  │
                    ┌─────────────────────────────────────────────┼─────────────────────────────────────────────┐
                    ▼                                             ▼                                             ▼
          [ Disease Service ]                             [ Crop Service ]                              [ Yield Service ]
          ├── Preprocessing                               ├── Preprocessing                             ├── Preprocessing
          ├── PyTorch (CNN/ViT)                           ├── Random Forest                             ├── Random Forest Regressor
          ├── Grad-CAM Heatmaps                           ├── SHAP Explanations                         ├── SHAP Explanations
          └── Uncertainty Estimation                      └── Probability Calibration                   └── Conformal Prediction Intervals
```

## Major Modules
* **Inference Serving API:** FastAPI application providing structured endpoints for validation, inference request handling, and error routing. Models are loaded once into memory on startup.
* **Disease Diagnosis Service:** Handles image validation, preprocessing (resizing, normalization), model inference, predictive entropy/MC dropout uncertainty calculations, and Grad-CAM generation.
* **Crop Recommendation Service:** Implements validation, preprocessing, classification inference, probability calibration (Isotonic Regression/Temperature Scaling), and local SHAP explanations.
* **Yield Prediction Service:** Processes agricultural input schemas, invokes the regression model, constructs Conformal Prediction uncertainty intervals, and generates SHAP feature contribution metrics.

## Communication Protocols
* **Frontend-to-Backend:** HTTP/1.1 REST client-server model.
  * Crop and Yield services exchange JSON payloads.
  * Disease Service utilizes `multipart/form-data` for image file uploads.

## Important Folders & Entry Points
* [api/](file:///Users/bramhabajannavar/Desktop/Major%20project/api/) — Backend code.
  * [api/main.py](file:///Users/bramhabajannavar/Desktop/Major%20project/api/main.py) — **Entry Point**: FastAPI application initialization and routing setup.
  * [api/routes/](file:///Users/bramhabajannavar/Desktop/Major%20project/api/routes/) — Specific route handlers for each pipeline.
* [models/](file:///Users/bramhabajannavar/Desktop/Major%20project/models/) — Core ML logic directories containing model definitions, inference wrappers, explanations, and uncertainty estimators.
* [app/](file:///Users/bramhabajannavar/Desktop/Major%20project/app/) — Streamlit frontend.
  * [app/streamlit_app.py](file:///Users/bramhabajannavar/Desktop/Major%20project/app/streamlit_app.py) — **Entry Point**: Streamlit application landing page and navigation menu.
* [artifacts/](file:///Users/bramhabajannavar/Desktop/Major%20project/artifacts/) — Pre-trained ML binaries, preprocessing parameters, class mappings, and model metadata.

## External Services
* **None:** The project is fully self-contained and run locally/within isolated Docker containers without relying on external cloud APIs.

## Major Dependencies
* **Web & Routing:** FastAPI, Uvicorn, Streamlit, Pydantic, HTTPX
* **Deep & Tabular ML:** PyTorch, Torchvision, scikit-learn
* **Explainability:** SHAP, Captum
* **General:** PyYAML, NumPy, Pandas, Pillow
