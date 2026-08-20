import os
import json
import time
import random
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Set seed
random.seed(42)
np.random.seed(42)

def train_yield_model(data_dir="data/yield", artifact_dir="artifacts/yield"):
    os.makedirs(artifact_dir, exist_ok=True)
    
    # Load data
    train_df = pd.read_csv(os.path.join(data_dir, "train.csv"))
    val_df = pd.read_csv(os.path.join(data_dir, "val.csv"))
    test_df = pd.read_csv(os.path.join(data_dir, "test.csv"))
    
    categorical_cols = ["crop", "season"]
    numeric_cols = ["rainfall", "temperature", "area"]
    target_col = "yield"
    
    X_train = train_df[categorical_cols + numeric_cols]
    y_train = train_df[target_col].values
    
    X_val = val_df[categorical_cols + numeric_cols]
    y_val = val_df[target_col].values
    
    X_test = test_df[categorical_cols + numeric_cols]
    y_test = test_df[target_col].values
    
    # Preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols),
            ("num", StandardScaler(), numeric_cols)
        ]
    )
    
    # Pipeline
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42))
        ]
    )
    
    # Train
    start_time = time.time()
    pipeline.fit(X_train, y_train)
    training_duration = time.time() - start_time
    
    # Predict on validation set to compute conformal residuals
    val_preds = pipeline.predict(X_val)
    conformal_residuals = np.abs(y_val - val_preds)
    
    # Predict on test set
    test_preds = pipeline.predict(X_test)
    
    # Calculate metrics
    mae = mean_absolute_error(y_test, test_preds)
    rmse = np.sqrt(mean_squared_error(y_test, test_preds))
    r2 = r2_score(y_test, test_preds)
    
    # Verify conformal coverage on test set at 90% confidence (alpha = 0.10)
    alpha = 0.10
    n_val = len(conformal_residuals)
    q_index = int(np.ceil((1.0 - alpha) * (n_val + 1))) - 1
    q_index = max(0, min(q_index, n_val - 1))
    q_hat = np.sort(conformal_residuals)[q_index]
    
    test_intervals_lower = test_preds - q_hat
    test_intervals_upper = test_preds + q_hat
    coverage = np.mean((y_test >= test_intervals_lower) & (y_test <= test_intervals_upper))
    mean_width = 2 * q_hat
    
    print(f"Test MAE: {mae:.4f}")
    print(f"Test RMSE: {rmse:.4f}")
    print(f"Test R2: {r2:.4f}")
    print(f"Conformal Coverage (90% Nominal): {coverage:.4f} (Mean Width: {mean_width:.4f})")
    
    # Save artifacts
    with open(os.path.join(artifact_dir, "model.pkl"), "wb") as f:
        pickle.dump(pipeline, f)
    with open(os.path.join(artifact_dir, "conformal_residuals.pkl"), "wb") as f:
        pickle.dump(conformal_residuals, f)
        
    metadata = {
        "model_name": "random_forest_regressor",
        "model_version": "yield_v1",
        "dataset": "CropAI Agricultural Yield Tabular Dataset",
        "trained_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "training_duration_seconds": round(training_duration, 2),
        "random_seed": 42,
        "features": {
            "categorical": categorical_cols,
            "numeric": numeric_cols
        },
        "metrics": {
            "mae": float(mae),
            "rmse": float(rmse),
            "r2": float(r2),
            "conformal_90_coverage": float(coverage),
            "conformal_90_interval_width": float(mean_width)
        }
    }
    
    with open(os.path.join(artifact_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=4)
        
    print("Yield prediction artifacts saved successfully!")

if __name__ == "__main__":
    train_yield_model()
