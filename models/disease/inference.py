import os
import io
import json
import torch
from PIL import Image
from torchvision import transforms

from models.disease.model import get_disease_model
from models.disease.uncertainty import calculate_mc_uncertainty
from models.disease.explainability import GradCAM, overlay_heatmap

class DiseaseInferenceService:
    def __init__(self, config_path="configs/config.yaml"):
        # Load config
        import yaml
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
            
        self.model_path = self.config["models"]["disease"]["path"]
        self.class_mapping_path = self.config["models"]["disease"]["class_mapping_path"]
        self.preprocessing_path = self.config["models"]["disease"]["preprocessing_path"]
        
        # Load class names
        with open(self.class_mapping_path, "r") as f:
            self.class_mapping = json.load(f)
            # Convert keys to integer
            self.class_mapping = {int(k): v for k, v in self.class_mapping.items()}
            
        # Load preprocessing config
        with open(self.preprocessing_path, "r") as f:
            self.pre_config = json.load(f)
            
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        
        # Instantiate model
        self.model = get_disease_model(num_classes=len(self.class_mapping))
        # Load weights
        self.model.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()
        
        # Preprocessing transform
        self.transform = transforms.Compose([
            transforms.Resize((self.pre_config["image_size"], self.pre_config["image_size"])),
            transforms.ToTensor(),
            transforms.Normalize(self.pre_config["mean"], self.pre_config["std"])
        ])
        
        # Set target layer for Grad-CAM
        # In torchvision MobileNetV3 small, the last conv of features is model.features[-1][0]
        self.target_layer = self.model.model.features[-1][0]

    def predict(self, image_bytes):
        # Open PIL Image
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Preprocess
        input_tensor = self.transform(image).unsqueeze(0) # add batch dim
        
        # Run uncertainty-aware inference (MC Dropout)
        avg_probs, uncertainty_info = calculate_mc_uncertainty(
            self.model, input_tensor, self.device, num_passes=10
        )
        
        # Get top class
        predicted_idx = int(avg_probs.argmax())
        prediction_label = self.class_mapping[predicted_idx]
        confidence = float(avg_probs[predicted_idx])
        
        # Get top predictions list
        top_predictions = []
        for idx, prob in enumerate(avg_probs):
            top_predictions.append({
                "class": self.class_mapping[idx],
                "probability": float(prob)
            })
        top_predictions = sorted(top_predictions, key=lambda x: x["probability"], reverse=True)
        
        # Generate Grad-CAM heatmaps
        # Note: We must temporarily put model back to eval (but keeping hooks)
        self.model.eval()
        grad_cam = GradCAM(self.model, self.target_layer)
        
        try:
            heatmap = grad_cam.generate_heatmap(input_tensor, predicted_idx)
            overlay_img = overlay_heatmap(image, heatmap, alpha=0.5)
            
            # Save overlay image to bytes
            img_byte_arr = io.BytesIO()
            overlay_img.save(img_byte_arr, format='PNG')
            overlay_bytes = img_byte_arr.getvalue()
        finally:
            grad_cam.remove_hooks()
            
        return {
            "prediction": prediction_label,
            "confidence": confidence,
            "top_predictions": top_predictions,
            "uncertainty": uncertainty_info,
            "overlay_bytes": overlay_bytes,
            "model_version": "disease_v1"
        }
