import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap

class YieldExplainer:
    def __init__(self, model_service):
        self.model_service = model_service
        self.pipeline = self.model_service.model
        self.preprocessor = self.pipeline.named_steps["preprocessor"]
        self.regressor = self.pipeline.named_steps["regressor"]
        
        # Instantiate TreeExplainer on the regressor
        self.explainer = shap.TreeExplainer(self.regressor)

    def explain_prediction(self, input_data: dict):
        # Convert to DataFrame
        df = pd.DataFrame([input_data])
        
        # Transform features using pipeline preprocessor
        X_transformed = self.preprocessor.transform(df)
        
        # Get feature names after OneHotEncoder expansion
        try:
            # get_feature_names_out returns array of strings
            feature_names_out = self.preprocessor.get_feature_names_out()
        except Exception:
            # Fallback if scikit-learn has issues
            feature_names_out = [f"feature_{i}" for i in range(X_transformed.shape[1])]
            
        # Compute SHAP values
        shap_values = self.explainer.shap_values(X_transformed)[0]
        
        # Create mapping
        contributions = []
        for i, name in enumerate(feature_names_out):
            # Clean up feature name (e.g., cat__crop_Rice -> crop_Rice)
            clean_name = name.replace("cat__", "").replace("num__", "")
            contributions.append({
                "feature": clean_name,
                "shap_value": float(shap_values[i])
            })
            
        # Sort by absolute SHAP value
        contributions = sorted(contributions, key=lambda x: abs(x["shap_value"]), reverse=True)
        return contributions

def generate_yield_shap_plot(contributions, predicted_yield):
<<<<<<< HEAD
    # Sort contributions by raw SHAP value
    sorted_contribs = sorted(contributions, key=lambda x: x["shap_value"])
    
    # Filter features that have non-zero SHAP impact (or keep top 10 to keep plot clean)
=======
    sorted_contribs = sorted(contributions, key=lambda x: x["shap_value"])
>>>>>>> origin/bhavya-feature
    filtered_contribs = [c for c in sorted_contribs if abs(c["shap_value"]) > 0.001][-10:]
    
    features = [c["feature"] for c in filtered_contribs]
    shap_vals = [c["shap_value"] for c in filtered_contribs]
<<<<<<< HEAD
    colors = ['#2ca02c' if v >= 0 else '#d62728' for v in shap_vals]
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(features, shap_vals, color=colors, edgecolor='none', height=0.6)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    ax.tick_params(colors='#666666')
    ax.axvline(0, color='#cccccc', linewidth=0.8, linestyle='--')
    
    plt.title(f"SHAP Feature Impact (Yield prediction: {predicted_yield:.2f} t/ha)", fontsize=11, fontweight='bold', pad=15, color='#333333')
    plt.xlabel("SHAP Value (Impact on yield prediction)", fontsize=9, color='#666666')
=======
    colors = ['#10b981' if v >= 0 else '#ef4444' for v in shap_vals]
    
    fig, ax = plt.subplots(figsize=(6, 3.5))
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    
    ax.barh(features, shap_vals, color=colors, edgecolor='none', height=0.55)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#88888844')
    ax.tick_params(colors='#888888', labelsize=9)
    ax.axvline(0, color='#88888844', linewidth=0.8, linestyle='--')
    
    plt.title(f"SHAP Feature Impact ({predicted_yield:.2f} t/ha)", fontsize=10, pad=12, color='#888888')
    plt.xlabel("SHAP Value (Impact)", fontsize=8, color='#888888')
>>>>>>> origin/bhavya-feature
    plt.tight_layout()
    
    return fig
