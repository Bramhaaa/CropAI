# CropAI Dataset Provenance and Specifications

This directory contains the datasets used to train and evaluate the machine learning models in CropAI.

---

## 1. Crop Leaf Disease Diagnosis Dataset
* **Dataset Name:** CropAI Synthetic Plant Pathology Image Dataset
* **Source:** Synthetically generated via [generate_datasets.py](file:///Users/bramhabajannavar/Desktop/Major%20project/data/generate_datasets.py) mimicking crop leaves with specific lesion structures.
* **License:** MIT License / Open Access (Synthetic)
* **Number of Samples:** 150 total (50 per class)
* **Number of Classes:** 3 classes:
  - `Tomato___healthy`
  - `Tomato___Early_blight`
  - `Tomato___Late_blight`
* **Splits:**
  - **Train:** 70% (35 images per class)
  - **Validation:** 15% (7 images per class)
  - **Test:** 15% (7 images per class)
* **Image Size:** 224x224 RGB
* **Preprocessing:** Normalized using ImageNet stats (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]).
* **Known Limitations:** The images are synthetic ellipses with noise. While suitable for training CNNs and testing Grad-CAM mappings in this workspace environment, they do not represent real-world clinical plant leaves.

---

## 2. Crop Recommendation Dataset
* **Dataset Name:** CropAI Tabular Soil & Environment Dataset
* **Source:** Synthetically generated via [generate_datasets.py](file:///Users/bramhabajannavar/Desktop/Major%20project/data/generate_datasets.py) based on standard crop recommendation distributions (similar to Kaggle's Crop Recommendation dataset).
* **License:** MIT License / Open Access (Synthetic)
* **Number of Samples:** 1,000 total samples
* **Features:** 7 numeric parameters:
  - `nitrogen` (mg/kg)
  - `phosphorus` (mg/kg)
  - `potassium` (mg/kg)
  - `temperature` (°C)
  - `humidity` (%)
  - `ph`
  - `rainfall` (mm)
* **Target Classes:** 7 crop types:
  - `Rice`, `Maize`, `Chickpea`, `Cotton`, `Mango`, `Banana`, `Grapes`
* **Splits:**
  - **Train:** 700 samples (70%)
  - **Validation:** 150 samples (15%)
  - **Test:** 150 samples (15%)
* **Preprocessing:** StandardScaler applied to numeric soil and environmental features.
* **Known Limitations:** Values are modeled on normal distributions with distinct means per crop class. Features are assumed to have independent variance.

---

## 3. Yield Prediction Dataset
* **Dataset Name:** CropAI Agricultural Yield Regression Dataset
* **Source:** Synthetically generated via [generate_datasets.py](file:///Users/bramhabajannavar/Desktop/Major%20project/data/generate_datasets.py) representing yields across different crops, seasons, areas, and environmental factors.
* **License:** MIT License / Open Access (Synthetic)
* **Number of Samples:** 1,000 total samples
* **Features:** 5 parameters:
  - `crop` (categorical, 7 unique values)
  - `season` (categorical, 4 unique values)
  - `rainfall` (numeric, mm)
  - `temperature` (numeric, °C)
  - `area` (numeric, hectares)
* **Target:** `yield` (numeric continuous, tonnes/hectare)
* **Splits:**
  - **Train:** 700 samples (70%)
  - **Validation:** 150 samples (15%)
  - **Test:** 150 samples (15%)
* **Preprocessing:** OneHotEncoding for categoricals (`crop`, `season`) and StandardScaler for numeric columns.
* **Known Limitations:** Yield is computed from simple deterministic equations with Gaussian noise added. Target leakage has been strictly avoided by ensuring area metrics do not imply harvest scale beyond scale scaling.
