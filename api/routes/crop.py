from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any

from api.dependencies import get_crop_service
from models.crop.inference import CropInferenceService
from models.crop.explainability import CropExplainer

router = APIRouter()

class CropRecommendRequest(BaseModel):
    nitrogen: float = Field(..., ge=0, le=200, description="Nitrogen content in soil (mg/kg)")
    phosphorus: float = Field(..., ge=0, le=200, description="Phosphorus content in soil (mg/kg)")
    potassium: float = Field(..., ge=0, le=300, description="Potassium content in soil (mg/kg)")
    temperature: float = Field(..., ge=-10, le=60, description="Air temperature (°C)")
    humidity: float = Field(..., ge=0, le=100, description="Relative humidity (%)")
    ph: float = Field(..., ge=0, le=14, description="Soil pH value")
    rainfall: float = Field(..., ge=0, le=1000, description="Annual/seasonal rainfall (mm)")

@router.post("/recommend")
async def recommend_crop(
    payload: CropRecommendRequest,
    service: CropInferenceService = Depends(get_crop_service)
) -> Dict[str, Any]:
    # Extract data as dict
    input_dict = payload.model_dump()
    
    # Run prediction
    try:
        result = service.predict(input_dict)
    except Exception as e:
        import logging
        logging.error(f"Inference error in crop route: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal inference engine failure.")
        
    # Generate SHAP explanations
    try:
        explainer = CropExplainer(service)
        contributions = explainer.explain_prediction(input_dict, result["recommended_crop"])
    except Exception as e:
        import logging
        logging.error(f"SHAP explanation error in crop route: {str(e)}", exc_info=True)
        contributions = []
        
    return {
        "recommended_crop": result["recommended_crop"],
        "confidence": result["confidence"],
        "top_recommendations": result["top_recommendations"],
        "reliability": result["reliability"],
        "explanation": {
            "top_features": contributions
        },
        "model_version": result["model_version"]
    }
