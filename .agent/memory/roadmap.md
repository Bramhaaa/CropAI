# CropAI — Product Roadmap

This document outlines the development trajectory of CropAI based on project scope constraints.

---

## Completed
* **AGENT.md & lifecycle workflows** defined.
* **Phase 1 — Onboarding & Structure Initialization:** Initialized project workspace, folder conventions, configurations, and memory baselines.
* **Phase 2 — Dataset Preparation:** Coded data generator and prepared splits partitioning for leaf images and soil/yield tabular datasets.
* **Phase 3 — Crop Disease Model:** Implemented PyTorch MobileNetV3 small classifier, Grad-CAM mapping, MC Dropout entropy, and ECE evaluation.
* **Phase 4 — Crop Recommendation Model:** Fitted RandomForestClassifier calibrated with isotonic regression, and computed local SHAP feature importances.
* **Phase 5 — Yield Prediction Model:** Coded RandomForestRegressor, mapped dynamic Conformal Prediction interval boundaries, and generated SHAP contributions.
* **Phase 6 — FastAPI Serving Layer:** Initialized FastAPI server, preloaded singletons on lifespan startup, implemented Pydantic validations, and logged request latency.
* **Phase 7 — Streamlit Frontend:** Designed multi-page dashboard representing slider forms, SHAP pyplot charts, and decoded image overlays.
* **Phase 8 — Integration & Bug-Fixing:** Conducted integration verification, fixed unpickling segfaults by migrating to RandomForest, and bypassed reserved word syntax errors.
* **Phase 9 — Dockerization:** Configured Dockerfile and docker-compose setups for containerized multi-service orchestrations.

---

## Planned / Future Scope
* **Phase 10 — Automated Retraining:** Integrate database pipeline with automatic model retraining and drift detection alerts.
* **Phase 11 — Cloud Scaling:** Deploy the dockerized application to cloud platforms (AWS ECS/EKS or GCP Cloud Run).
