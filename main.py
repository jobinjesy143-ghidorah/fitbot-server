from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any

app = FastAPI(title="FitBot Intelligence Engine")

class ScanRequest(BaseModel):
    username: str
    anchor_height_inches: float
    segment: str
    concept: str
    category: str
    
    shoulders: Optional[float] = None
    chest: Optional[float] = None
    waist: Optional[float] = None
    hips: Optional[float] = None
    
    left_shoulder: Optional[Dict[str, float]] = None
    right_shoulder: Optional[Dict[str, float]] = None
    left_hip: Optional[Dict[str, float]] = None
    right_hip: Optional[Dict[str, float]] = None

# 1. The Default Root Route
@app.get("/")
def root_check():
    return {"status": "online"}

# 2. THE FIX: The exact route Render is looking for to keep the server alive!
@app.get("/health")
def health_check():
    return {"status": "healthy", "code": 200}

@app.post("/analyze")
async def analyze_profile(req: ScanRequest):
    shape_result = req.category

    if shape_result.lower() == "none" or shape_result == "":
        if req.shoulders and req.hips:
            diff = req.shoulders - req.hips
            if diff > 2.0:
                shape_result = "Inverted Triangle"
            elif diff < -2.0:
                shape_result = "Pear"
            else:
                shape_result = "Hourglass"
        elif req.left_shoulder and req.left_hip:
            shape_result = "Athletic Rectangle"
        else:
            shape_result = "Proportional"

    products_list = [
        {
            "name": f"Premium {req.concept} Jacket ({req.segment})",
            "brand": "NIFT Signature Collection",
            "price": "45.00",
            "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&q=80",
            "product_url": "https://www.google.com/search?q=jacket"
        },
        {
            "name": f"Intelligent Fit Trousers for {shape_result}",
            "brand": "FutureWear",
            "price": "35.50",
            "image_url": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=500&q=80",
            "product_url": "https://www.google.com/search?q=trousers"
        },
        {
            "name": f"Engineered Cotton Tee ({req.concept})",
            "brand": "Zero Waste Studios",
            "price": "22.99",
            "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&q=80",
            "product_url": "https://www.google.com/search?q=t-shirt"
        }
    ]

    return {
        "shape": shape_result,
        "products": products_list
    }
