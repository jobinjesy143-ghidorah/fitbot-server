from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, List

app = FastAPI(title="FitBot Intelligence Engine - Production")

# --- 1. DATA MODELS ---
class ScanRequest(BaseModel):
    username: str
    anchor_height_inches: float
    segment: str
    concept: str
    category: str
    
    # Optional Manual Inputs
    shoulders: Optional[float] = None
    chest: Optional[float] = None
    waist: Optional[float] = None
    hips: Optional[float] = None
    
    # Optional Camera Inputs
    left_shoulder: Optional[Dict[str, float]] = None
    right_shoulder: Optional[Dict[str, float]] = None
    left_hip: Optional[Dict[str, float]] = None
    right_hip: Optional[Dict[str, float]] = None

# --- 2. STARTUP PRODUCT CATALOG (Mock Database) ---
# In the future, this will be replaced by a live connection to PostgreSQL or Firebase.
# For now, it acts as your live inventory, tagged by body shape and concept.
CATALOG = [
    # WOMENSWEAR - CASUAL
    {
        "name": "Cinched Waist Wrap Dress", "brand": "Zara", "price": "59.90",
        "image_url": "https://images.unsplash.com/photo-1591369822096-ffd140ec948f?w=500&q=80",
        "product_url": "https://www.zara.com",
        "target_shapes": ["Hourglass", "Rectangle"], "segment": "Womenswear", "concept": "Casual"
    },
    {
        "name": "A-Line Midi Skirt", "brand": "H&M", "price": "34.99",
        "image_url": "https://images.unsplash.com/photo-1583496661160-c588c4af15f3?w=500&q=80",
        "product_url": "https://www.hm.com",
        "target_shapes": ["Inverted Triangle", "Apple"], "segment": "Womenswear", "concept": "Casual"
    },
    {
        "name": "High-Rise Straight Cut Denim", "brand": "Levi's", "price": "89.50",
        "image_url": "https://images.unsplash.com/photo-1542272604-780c40fb320e?w=500&q=80",
        "product_url": "https://www.levi.com",
        "target_shapes": ["Pear", "Hourglass", "Spoon"], "segment": "Womenswear", "concept": "Casual"
    },
    
    # WOMENSWEAR - FORMAL
    {
        "name": "Structured Shoulder Blazer", "brand": "Mango", "price": "119.99",
        "image_url": "https://images.unsplash.com/photo-1548624149-f9b1859aa7d0?w=500&q=80",
        "product_url": "https://shop.mango.com",
        "target_shapes": ["Pear", "Spoon", "Rectangle"], "segment": "Womenswear", "concept": "Formal"
    },
    {
        "name": "Deep V-Neck Silk Blouse", "brand": "Massimo Dutti", "price": "95.00",
        "image_url": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500&q=80",
        "product_url": "https://www.massimodutti.com",
        "target_shapes": ["Inverted Triangle", "Apple", "Rectangle"], "segment": "Womenswear", "concept": "Formal"
    },

    # MENSWEAR - CASUAL
    {
        "name": "Tapered Cargo Joggers", "brand": "Nike", "price": "75.00",
        "image_url": "https://images.unsplash.com/photo-1617137968427-85924c800a22?w=500&q=80",
        "product_url": "https://www.nike.com",
        "target_shapes": ["Inverted Triangle", "Rectangle", "Athletic"], "segment": "Menswear", "concept": "Casual"
    },
    {
        "name": "Classic Relaxed Fit Tee", "brand": "Uniqlo", "price": "19.90",
        "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&q=80",
        "product_url": "https://www.uniqlo.com",
        "target_shapes": ["Apple", "Pear", "Rectangle"], "segment": "Menswear", "concept": "Casual"
    },

    # MENSWEAR - FORMAL
    {
        "name": "Slim Fit Oxford Shirt", "brand": "Ralph Lauren", "price": "125.00",
        "image_url": "https://images.unsplash.com/photo-1596755094514-f87e32f85e2c?w=500&q=80",
        "product_url": "https://www.ralphlauren.com",
        "target_shapes": ["Athletic", "Inverted Triangle", "Hourglass"], "segment": "Menswear", "concept": "Formal"
    }
]

# --- 3. CORE ENDPOINTS ---
@app.get("/")
def root_check():
    return {"status": "online", "mode": "production"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "code": 200}

@app.post("/analyze")
async def analyze_profile(req: ScanRequest):
    shape_result = req.category.strip().title()

    # Calculate Shape dynamically if the client sent 'None' (Camera/Manual mode)
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
            shape_result = "Athletic" # Simplified generic for 3D mapping
        else:
            shape_result = "Rectangle"

    # --- THE RECOMMENDATION ENGINE ---
    # Filter the catalog based on the exact user metrics
    recommended_products = []
    
    for item in CATALOG:
        # 1. Check Segment (Gender) Match
        if req.segment.lower() != item["segment"].lower() and item["segment"] != "Unisex":
            continue
            
        # 2. Check Concept (Vibe) Match
        if req.concept.lower() != item["concept"].lower() and req.concept.lower() != "any":
            continue
            
        # 3. Check Shape Geometry Match
        # Only add the product if the user's shape is in the product's target list
        if shape_result not in item["target_shapes"] and "All" not in item["target_shapes"]:
            continue
            
        recommended_products.append(item)

    # Fallback Mechanism: If the catalog is too small and yields 0 matches for a specific combo
    if len(recommended_products) == 0:
        recommended_products = [
            {
                "name": f"Universal Fit Essential ({req.concept})",
                "brand": "FitBot Basics",
                "price": "29.99",
                "image_url": "https://images.unsplash.com/photo-1620799140188-3b2a02fd9a77?w=500&q=80",
                "product_url": "https://google.com"
            }
        ]

    # Return exactly what Flutter expects
    return {
        "shape": shape_result,
        "products": recommended_products
    }
