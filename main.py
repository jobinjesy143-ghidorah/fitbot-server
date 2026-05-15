from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI(title="FitBot Intelligence Engine - Production")

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

# ✅ STARTUP CATALOG: Uses hyper-stable image generators instead of brittle Unsplash IDs
CATALOG = [
    # WOMENSWEAR - CASUAL
    {"name": "Cinched Waist Wrap Dress", "brand": "Zara", "price": "59.90", "image_url": "https://picsum.photos/seed/zara1/500/800", "product_url": "https://www.zara.com", "target_shapes": ["Hourglass", "Rectangle"], "segment": "Womenswear", "concept": "Casual"},
    {"name": "A-Line Midi Skirt", "brand": "H&M", "price": "34.99", "image_url": "https://picsum.photos/seed/hm2/500/800", "product_url": "https://www.hm.com", "target_shapes": ["Inverted Triangle", "Apple"], "segment": "Womenswear", "concept": "Casual"},
    {"name": "High-Rise Straight Cut Denim", "brand": "Levi's", "price": "89.50", "image_url": "https://picsum.photos/seed/levis3/500/800", "product_url": "https://www.levi.com", "target_shapes": ["Pear", "Hourglass", "Spoon"], "segment": "Womenswear", "concept": "Casual"},
    
    # WOMENSWEAR - FORMAL
    {"name": "Structured Shoulder Blazer", "brand": "Mango", "price": "119.99", "image_url": "https://picsum.photos/seed/mango4/500/800", "product_url": "https://shop.mango.com", "target_shapes": ["Pear", "Spoon", "Rectangle"], "segment": "Womenswear", "concept": "Formal"},
    {"name": "Deep V-Neck Silk Blouse", "brand": "Massimo Dutti", "price": "95.00", "image_url": "https://picsum.photos/seed/massimo5/500/800", "product_url": "https://www.massimodutti.com", "target_shapes": ["Inverted Triangle", "Apple", "Rectangle"], "segment": "Womenswear", "concept": "Formal"},
    
    # MENSWEAR - CASUAL
    {"name": "Tapered Cargo Joggers", "brand": "Nike", "price": "75.00", "image_url": "https://picsum.photos/seed/nike6/500/800", "product_url": "https://www.nike.com", "target_shapes": ["Inverted Triangle", "Rectangle", "Athletic"], "segment": "Menswear", "concept": "Casual"},
    {"name": "Classic Relaxed Fit Tee", "brand": "Uniqlo", "price": "19.90", "image_url": "https://picsum.photos/seed/uniqlo7/500/800", "product_url": "https://www.uniqlo.com", "target_shapes": ["Apple", "Pear", "Rectangle"], "segment": "Menswear", "concept": "Casual"},
    
    # MENSWEAR - FORMAL
    {"name": "Slim Fit Oxford Shirt", "brand": "Ralph Lauren", "price": "125.00", "image_url": "https://picsum.photos/seed/ralph8/500/800", "product_url": "https://www.ralphlauren.com", "target_shapes": ["Athletic", "Inverted Triangle", "Hourglass"], "segment": "Menswear", "concept": "Formal"},
    {"name": "Tailored Wool Suit Jacket", "brand": "SuitSupply", "price": "399.00", "image_url": "https://picsum.photos/seed/suit9/500/800", "product_url": "https://suitsupply.com", "target_shapes": ["Pear", "Rectangle", "Athletic"], "segment": "Menswear", "concept": "Formal"}
]

@app.get("/")
def root_check():
    return {"status": "online"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "code": 200}

@app.post("/analyze")
async def analyze_profile(req: ScanRequest):
    shape_result = req.category.strip().title()

    if shape_result.lower() == "none" or shape_result == "":
        if req.shoulders and req.hips:
            diff = req.shoulders - req.hips
            if diff > 2.0:
                shape_result = "Inverted Triangle"
            elif diff < -2.0:
                shape_result = "Pear"
            else:
                shape_result = "Hourglass"
        else:
            shape_result = "Rectangle"

    recommended_products = []
    
    for item in CATALOG:
        if req.segment.lower() != item["segment"].lower() and item["segment"] != "Unisex":
            continue
        if req.concept.lower() != item["concept"].lower() and req.concept.lower() != "any":
            continue
        if shape_result not in item["target_shapes"] and "All" not in item["target_shapes"]:
            continue
        recommended_products.append(item)

    if len(recommended_products) == 0:
        recommended_products = [
            {"name": f"Universal Fit Essential ({req.concept})", "brand": "FitBot Basics", "price": "29.99", "image_url": "https://picsum.photos/seed/fallback/500/800", "product_url": "https://google.com"}
        ]

    return {"shape": shape_result, "products": recommended_products}
