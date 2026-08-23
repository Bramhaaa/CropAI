# CropAI — Semantic Project Index

This file lists the main features of the CropAI project. Future AI sessions should always read this file before searching the repository.

---

## 1. Crop Leaf Disease Diagnosis

* **Purpose:** Classify uploaded crop leaf images to identify specific diseases, calculate prediction confidence, estimate reliability/uncertainty, and produce visual region-of-interest heatmaps.
* **Folders:**
  - [models/disease/](file:///Users/bramhabajannavar/Desktop/Major%20project/models/disease/) — Preprocessing, modeling, Grad-CAM, and predictive entropy uncertainty.
* **Files:**
  - [models/disease/model.py](file:///Users/bramhabajannavar/Desktop/Major%20project/models/disease/model.py) — MobileNetV3 PyTorch class definition.
  - [models/disease/inference.py](file:///Users/bramhabajannavar/Desktop/Major%20project/models/disease/inference.py) — Image preprocessing and classification inference wrapper.
  - [models/disease/explainability.py](file:///Users/bramhabajannavar/Desktop/Major%20project/models/disease/explainability.py) — Grad-CAM visual heatmap generator and PIL overlays.
  - [models/disease/uncertainty.py](file:///Users/bramhabajannavar/Desktop/Major%20project/models/disease/uncertainty.py) — MC Dropout average probability and predictive entropy.
  - [api/routes/disease.py](file:///Users/bramhabajannavar/Desktop/Major%20project/api/routes/disease.py) — Multipart image upload endpoint handler.
  - [app/pages/disease.py](file:///Users/bramhabajannavar/Desktop/Major%20project/app/pages/disease.py) — Image uploader UI and overlay renderer.
* **Dependencies:** PyTorch, Torchvision, Matplotlib, Pillow
* **Examples:** Uploading a tomato leaf image to identify Late Blight, rendering a Grad-CAM overlay highlighting visual lesions.

---

## 2. Crop Recommendation

* **Purpose:** Suggest suitable crops based on soil composition and environmental metrics, displaying confidence scores and listing which factors drove the recommendation.
* **Folders:**
  - [models/crop/](file:///Users/bramhabajannavar/Desktop/Major%20project/models/crop/) — Recommendation classification, calibration, and SHAP.
* **Files:**
  - [models/crop/inference.py](file:///Users/bramhabajannavar/Desktop/Major%20project/models/crop/inference.py) — RandomForestClassifier loader and prediction confidence retrieval.
  - [models/crop/explainability.py](file:///Users/bramhabajannavar/Desktop/Major%20project/models/crop/explainability.py) — TreeExplainer interface and horizontal SHAP bar plotting.
  - [api/routes/crop.py](file:///Users/bramhabajannavar/Desktop/Major%20project/api/routes/crop.py) — Soil parameter recommendation endpoint handler.
  - [app/pages/crop.py](file:///Users/bramhabajannavar/Desktop/Major%20project/app/pages/crop.py) — Soil parameters UI sliders and SHAP chart display.
* **Dependencies:** scikit-learn, SHAP, Pandas, NumPy, Matplotlib
* **Examples:** Submitting soil N: 90, P: 42, K: 43 to obtain "Rice" with an explanation highlighting rainfall and humidity as positive contributions.

---

## 3. Yield Prediction

* **Purpose:** Estimate expected crop yield based on agricultural inputs, outputting a numerical prediction along with a Conformal Prediction interval defining the boundary of uncertainty.
* **Folders:**
  - [models/yield/](file:///Users/bramhabajannavar/Desktop/Major%20project/models/yield/) — Preprocessing pipeline, regression modeling, conformal prediction, and SHAP.
* **Files:**
  - [models/yield/inference.py](file:///Users/bramhabajannavar/Desktop/Major%20project/models/yield/inference.py) — RandomForestRegressor and Conformal Prediction interval boundaries mapper.
  - [models/yield/explainability.py](file:///Users/bramhabajannavar/Desktop/Major%20project/models/yield/explainability.py) — Regression feature preprocessor, SHAP explainer, and bar plotting.
  - [api/routes/yield.py](file:///Users/bramhabajannavar/Desktop/Major%20project/api/routes/yield.py) — Agricultural yield prediction endpoint handler.
  - [app/pages/yield.py](file:///Users/bramhabajannavar/Desktop/Major%20project/app/pages/yield.py) — Yield parameters UI select boxes and conformal interval displays.
* **Dependencies:** scikit-learn, SHAP, NumPy, Pandas, Matplotlib
* **Examples:** Entering Crop: Rice, Season: Kharif to predict 4.82 tonnes/hectare with a 90% confidence range of [4.12, 5.54] tonnes/hectare.

---

## 4. API & Application Serving Infrastructure

* **Purpose:** Load models once into memory on start, expose endpoints under `/api/v1/`, handle incoming inference calls, execute validation checks, and serve client pages.
* **Folders:**
  - [api/](file:///Users/bramhabajannavar/Desktop/Major%20project/api/) — FastAPI initialization, CORS configuration, dependency injection, and Pydantic validation schemas.
  - [app/](file:///Users/bramhabajannavar/Desktop/Major%20project/app/) — Streamlit frontend entry point, navigation rules, and styling modules.
  - [artifacts/](file:///Users/bramhabajannavar/Desktop/Major%20project/artifacts/) — Directories containing exported `.pkl` or `.pt` model binaries, feature scalers, encoders, and config metadata.
* **Files:**
  - [api/main.py](file:///Users/bramhabajannavar/Desktop/Major%20project/api/main.py) — FastAPI lifespan models caching and route setup.
  - [api/dependencies.py](file:///Users/bramhabajannavar/Desktop/Major%20project/api/dependencies.py) — Dependency injection singleton service instances loader.
  - [app/streamlit_app.py](file:///Users/bramhabajannavar/Desktop/Major%20project/app/streamlit_app.py) — Streamlit landing page and dashboard.
* **Dependencies:** FastAPI, Uvicorn, Streamlit, PyYAML, Docker
* **Examples:** Starting the application stack using `docker-compose up` to run both backend and frontend.
