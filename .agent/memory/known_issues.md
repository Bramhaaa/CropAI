# CropAI — Known Issues

This document records confirmed issues, missing implementations, and developer warnings.

---

## 1. Missing Implementations
* **None:** All core directories, model artifacts, serving services, automated tests, template files, and docker configurations have been successfully implemented.

## 2. Warnings
* **Target Leakage Warning (Yield Prediction):** Feature selection for the yield model must strictly filter out columns reflecting post-harvest variables or variables generated after target execution to avoid artificial model performance inflate.
