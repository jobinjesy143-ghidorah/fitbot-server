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

# --- COMMERCIAL FASHION CATALOG ---
# Using 100% verified, stable fashion photography URLs
CATALOG = [
    # WOMENSWEAR - CASUAL
    {"name": "Cinched Waist Wrap Dress", "brand": "Zara", "price": "59.90", "image_url": "https://images.unsplash.com/photo-1612336307429-8a898d10e223?auto=format&fit=crop&w=500&q=80", "product_url": "https://www.zara.com", "target_shapes": ["Hourglass", "Rectangle"], "segment": "Womenswear", "concept": "Casual"},
    {"name": "A-Line Midi Skirt", "brand": "H&M", "price": "34.99", "image_url": "https://images.unsplash.com/photo-1583496661160-c588c4af15f3?auto=format&fit=crop&w=500&q=80", "product_url": "https://www.hm.com", "target_shapes": ["Inverted Triangle", "Apple"], "segment": "Womenswear", "concept": "Casual"},
    {"name": "High-Rise Straight Cut Denim", "brand": "Levi's", "price": "89.50", "image_url": "https://images.unsplash.com/photo-1542272604-780c40fb320e?auto=format&fit=crop&w=500&q=80", "product_url": "https://www.levi.com", "target_shapes": ["Pear", "Hourglass", "Spoon"], "segment": "Womenswear", "concept": "Casual"},
    {"name": "Oversized Graphic Tee", "brand": "Urban Outfitters", "price": "35.00", "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=500&q=80", "product_url": "https://www.urbanoutfitters.com", "target_shapes": ["Rectangle", "Inverted Triangle", "Apple"], "segment": "Womenswear", "concept": "Casual"},
    
    # WOMENSWEAR - FORMAL
    {"name": "Structured Shoulder Blazer", "brand": "Mango", "price": "119.99", "image_url": "https://images.unsplash.com/photo-1548624149-f9b1859aa7d0?auto=format&fit=crop&w=500&q=80", "product_url": "https://shop.mango.com", "target_shapes": ["Pear", "Spoon", "Rectangle"], "segment": "Womenswear", "concept": "Formal"},
    {"name": "Tailored Wide-Leg Trousers", "brand": "Everlane", "price": "128.00", "image_url": "https://images.unsplash.com/photo-1509631179647-0c500ab14c55?auto=format&fit=crop&w=500&q=80", "product_url": "https://www.everlane.com", "target_shapes": ["Hourglass", "Pear"], "segment": "Womenswear", "concept": "Formal"},
    
    # WOMENSWEAR - STREETWEAR
    {"name": "Parachute Cargo Pants", "brand": "Jaded London", "price": "90.00", "image_url": "https://images.unsplash.com/photo-1617137968427-85924c800a22?auto=format&fit=crop&w=500&q=80", "product_url": "https://jadedldn.com", "target_shapes": ["Inverted Triangle", "Rectangle", "Apple"], "segment": "Womenswear", "concept": "Streetwear"},
    
    # MENSWEAR - CASUAL
    {"name": "Tapered Cargo Joggers", "brand": "Nike", "price": "75.00", "image_url": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=500&q=80", "product_url": "https://www.nike.com", "target_shapes": ["Inverted Triangle", "Rectangle", "Athletic"], "segment": "Menswear", "concept": "Casual"},
    {"name": "Classic Relaxed Fit Tee", "brand": "Uniqlo", "price": "19.90", "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=500&q=80", "product_url": "https://www.uniqlo.com", "target_shapes": ["Apple", "Pear", "Rectangle"], "segment": "Menswear", "concept": "Casual"},
    {"name": "Slim Fit Denim Jeans", "brand": "Diesel", "price": "150.00", "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=500&q=80", "product_url": "https://www.diesel.com", "target_shapes": ["Athletic", "Inverted Triangle"], "segment": "Menswear", "concept": "Casual"},
    
    # MENSWEAR - FORMAL
    {"name": "Slim Fit Oxford Shirt", "brand": "Ralph Lauren", "price": "125.00", "image_url": "https://images.unsplash.com/photo-1596755094514-f87e32f85e2c?auto=format&fit=crop&w=500&q=80", "product_url": "https://www.ralphlauren.com", "target_shapes": ["Athletic", "Inverted Triangle", "Hourglass"], "segment": "Menswear", "concept": "Formal"},
    {"name": "Tailored Wool Suit Jacket", "brand": "SuitSupply", "price": "399.00", "image_url": "https://images.unsplash.com/photo-1594938298598-70f70fc67120?auto=format&fit=crop&w=500&q=80", "product_url": "https://suitsupply.com", "target_shapes": ["Pear", "Rectangle", "Athletic"], "segment": "Menswear", "concept": "Formal"}
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

    # Dynamic Math Calculation
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
            shape_result = "Athletic" 
        else:
            shape_result = "Rectangle"

    recommended_products = []
    
    # High-Performance Filtering
    for item in CATALOG:
        if req.segment.lower() != item["segment"].lower() and item["segment"] != "Unisex":
            continue
        if req.concept.lower() != item["concept"].lower() and req.concept.lower() != "any":
            continue
        if shape_result not in item["target_shapes"] and "All" not in item["target_shapes"]:
            continue
        recommended_products.append(item)

    # Universal Fallback (if they select a wildly obscure combo)
    if len(recommended_products) == 0:
        recommended_products = [
            {
                "name": f"FitBot Premium Essential ({req.concept})", 
                "brand": "FitBot Core", 
                "price": "29.99", 
                "image_url": "https://images.unsplash.com/photo-1620799140188-3b2a02fd9a77?auto=format&fit=crop&w=500&q=80", 
                "product_url": "https://google.com"
            }
        ]

    return {"shape": shape_result, "products": recommended_products}
