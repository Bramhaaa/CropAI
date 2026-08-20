# CropAI — Project Overview

## Project Purpose
CropAI is an explainable, uncertainty-aware agricultural decision-support platform designed to assist farmers, agricultural students/researchers, and agricultural professionals in making informed crop management and farming choices.

## Overall Goal
Provide an accessible web application interface containing three independent and robust machine learning pipelines (disease diagnosis, crop recommendation, and yield prediction) that deliver reliable predictions, clear visual explanations, and calibrated uncertainty estimates.

## Major Features
* **Crop Disease Diagnosis:** leaf disease identification from images with Grad-CAM visual heatmaps, confidence scores, and uncertainty analysis.
* **Crop Recommendation:** data-driven crop recommendations from soil and environmental metrics (N, P, K, pH, rainfall, temperature, humidity) with SHAP feature contribution charts.
* **Yield Prediction:** regression modeling for expected crop yield with Conformal Prediction intervals (uncertainty boundary) and SHAP feature importance analysis.
* **ML API:** modular FastAPI serving layer keeping trained models loaded in memory for low-latency inference.
* **Web UI:** Streamlit frontend connecting to the FastAPI backend for intuitive end-user interactions.

## Technologies
* **Programming Languages:** Python
* **Backend Framework:** FastAPI, Uvicorn
* **Frontend UI Framework:** Streamlit
* **Machine Learning Stack:** PyTorch (CNN/ViT), scikit-learn, XGBoost, SHAP, Captum (Grad-CAM)
* **Deployment Target:** Docker, Docker Compose

## Current Maturity
* **Current Status:** Phase 8 — Completed / Production Ready.
* **Details:** All core machine learning models (disease, recommendation, yield), FastAPI serving endpoints, Streamlit dashboard pages, explainability charts, uncertainty quantification boundaries, tests, and Docker files are fully implemented and validated.
