import os
import requests
import math
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict

# Initializing the App
app = FastAPI(
    title="FitBot Pro Business Engine",
    description="Production-grade biometric and styling API",
    version="2.0.1"
)

# ✅ Enterprise CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATA MODELS ---
class ScanRequest(BaseModel):
    username: str
    left_shoulder: Optional[dict] = None
    right_shoulder: Optional[dict] = None
    anchor_height_inches: float
    segment: str 
    concept: str 
    category: str = "none"

# --- THE SEARCH ENGINE SERVICE ---
class ProductSearchService:
    @staticmethod
    def get_real_products(shape: str, concept: str, segment: str):
        query_map = {
            "Hourglass": f"high waisted {concept} {segment} outfit",
            "Inverted Triangle": f"V-neck {concept} {segment} top and A-line skirt",
            "Spoon": f"boatneck {concept} {segment} top and wide leg trousers",
            "Rectangle": f"peplum {concept} {segment} top and tapered pants",
            "Trapezoid": f"fitted {concept} {segment} shirt and chinos",
        }
        
        search_query = query_map.get(shape, f"{concept} {segment} outfit")
        api_key = os.getenv("SERPAPI_KEY")
        
        if not api_key:
            print("WARNING: SERPAPI_KEY missing in environment variables.")
            return []

        url = "https://serpapi.com/search.json"
        params = {
            "engine": "google_shopping",
            "q": search_query,
            "location": "India",
            "hl": "en",
            "gl": "in",
            "api_key": api_key
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            results = response.json().get("shopping_results", [])
            
            formatted_recs = []
            for item in results[:3]:
                formatted_recs.append({
                    "variation": f"TOP MATCH: {item.get('source', 'Retailer')}",
                    "garment": item.get("title", "Selected Piece"),
                    "image_path": item.get("thumbnail"),
                    "price": item.get("price"),
                    "product_link": item.get("link"),
                    "shape_metrics": f"Curated for {shape} silhouettes.",
                    "fabric_science": "Material details available on retailer site.",
                    "suggested_color": f"Price: {item.get('price')}"
                })
            return formatted_recs
        except Exception as e:
            print(f"Search Service Error: {e}")
            return []

# --- 🏠 ROOT ENDPOINT (Prevents 404 Log Spam) ---
@app.get("/")
async def root():
    return {
        "message": "FitBot Pro API is Online",
        "status": "active",
        "endpoints": ["/health", "/analyze"]
    }

# --- 🟢 RENDER HEALTH CHECK (Required for 'Live' status) ---
@app.get("/health")
async def health_check():
    return {"status": "online", "timestamp": time.time()}

# --- 🚀 MAIN API ROUTE ---
@app.post("/analyze")
async def analyze_and_search(request: ScanRequest):
    try:
        # 1. Biometric Logic (Smartphone Focal Calibration)
        s_w = 16.5 
        if request.left_shoulder and request.right_shoulder:
            # Calculate pixel distance on the X-axis
            px_dist = abs(request.right_shoulder['x'] - request.left_shoulder['x'])
            # Scale pixels to inches based on height anchor
            s_w = round((px_dist * 0.026) * (request.anchor_height_inches / 65.0), 1)

        # 2. Body Shape Identification
        shape = request.category if request.category != "none" else "Rectangle"
        if s_w > 18: 
            shape = "Inverted Triangle"
        
        # 3. Dynamic Product Sourcing
        recommendations = ProductSearchService.get_real_products(shape, request.concept, request.segment)

        return {
            "shape": shape,
            "recommendations": recommendations,
            "measurements_in": {
                "shoulders": s_w, 
                "waist": 28.0, 
                "hips": 36.0
            }
        }
    except Exception as e:
        print(f"Analysis Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Engine Error")
