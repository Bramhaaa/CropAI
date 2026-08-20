import os
import pickle
import numpy as np
import pandas as pd

class YieldInferenceService:
    def __init__(self, config_path="configs/config.yaml"):
        # Load config
        import yaml
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
            
        self.model_path = self.config["models"]["yield"]["path"]
        self.residuals_path = self.config["models"]["yield"]["conformal_residuals_path"]
        
        # Load artifacts
        with open(self.model_path, "rb") as f:
            self.model = pickle.load(f)
        with open(self.residuals_path, "rb") as f:
            self.conformal_residuals = pickle.load(f)
            
        self.categorical_cols = ["crop", "season"]
        self.numeric_cols = ["rainfall", "temperature", "area"]

    def predict(self, input_data: dict, confidence_level: float = 0.90):
        """
        Input: dict with keys: crop, season, rainfall, temperature, area.
        """
        # Convert to DataFrame
        df = pd.DataFrame([input_data])
        
        # Make base prediction
        pred = float(self.model.predict(df)[0])
        
        # Calculate conformal interval
        alpha = 1.0 - confidence_level
        n_val = len(self.conformal_residuals)
        q_index = int(np.ceil((1.0 - alpha) * (n_val + 1))) - 1
        q_index = max(0, min(q_index, n_val - 1))
        q_hat = float(np.sort(self.conformal_residuals)[q_index])
        
        lower_bound = max(0.0, pred - q_hat) # Yield cannot be negative
        upper_bound = pred + q_hat
        
        # Features map for explainability reference
        return {
            "predicted_yield": pred,
            "unit": "tonnes/hectare",
            "interval": {
                "lower": lower_bound,
                "upper": upper_bound,
                "confidence_level": confidence_level,
                "interval_width": float(q_hat * 2)
            },
            "features": input_data,
            "model_version": "yield_v1"
        }
