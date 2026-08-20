# CropAI — Architectural Decisions

This file logs key structural and design choices made during the development of CropAI.

---

## 1. Documentation-First Memory System
* **Date:** 2026-08-20
* **Context:** AI sessions require persistent context to prevent repetitive repository scanning and minimize discovery latency.
* **Decision Made:** Established a structured agent folder layout under `.agent/` mapping guidelines, memory logs, templates, and workflows.
* **Reasoning:** Storing contextual summaries separate from the primary code maintains a clear structure and assists future AI agents.
* **Consequences:** All future sessions must follow `AGENT.md` guidelines, consulting the semantic index and updating memory upon session closure.

---

## 2. Decoupled Interface and ML API Service
* **Date:** 2026-08-20
* **Context:** The Streamlit user interface must not couple directly with ML models to ensure flexibility and ease of scaling.
* **Decision Made:** Adopted an API-first design where Streamlit interacts only with FastAPI via HTTP REST protocols; FastAPI handles all model loading and inference logic.
* **Reasoning:** Keeps model serving separated from the visualization layout, permitting independent updates and potential remote service migrations.
* **Consequences:** Endpoints must return standardized schemas, and Streamlit pages must communicate strictly via HTTP calls to FastAPI.

---

## 3. Explainability and Uncertainty as Core Requirements
* **Date:** 2026-08-20
* **Context:** Crop classification and yield prediction are high-consequence decisions where raw prediction scores can be misleading.
* **Decision Made:** mandated explainability tools (Grad-CAM, SHAP) and calibration/uncertainty estimators (MC Dropout, Conformal Prediction) alongside standard inference.
* **Reasoning:** Encourages transparency, informs the user of prediction limitations, and indicates spatial/feature contributions in the UI.
* **Consequences:** Models cannot be deployed without exporting metadata regarding confidence calibration and explanation availability.
