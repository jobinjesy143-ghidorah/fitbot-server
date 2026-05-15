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

# --- MASSIVE PRODUCTION CATALOG ---
CATALOG = [
    # WOMENSWEAR - CASUAL
    {"name": "Cinched Waist Wrap Dress", "brand": "Zara", "price": "59.90", "image_url": "https://images.unsplash.com/photo-1591369822096-ffd140ec948f?w=500&q=80", "product_url": "https://www.zara.com", "target_shapes": ["Hourglass", "Rectangle"], "segment": "Womenswear", "concept": "Casual"},
    {"name": "A-Line Midi Skirt", "brand": "H&M", "price": "34.99", "image_url": "https://images.unsplash.com/photo-1583496661160-c588c4af15f3?w=500&q=80", "product_url": "https://www.hm.com", "target_shapes": ["Inverted Triangle", "Apple"], "segment": "Womenswear", "concept": "Casual"},
    {"name": "High-Rise Straight Cut Denim", "brand": "Levi's", "price": "89.50", "image_url": "https://images.unsplash.com/photo-1542272604-780c40fb320e?w=500&q=80", "product_url": "https://www.levi.com", "target_shapes": ["Pear", "Hourglass", "Spoon"], "segment": "Womenswear", "concept": "Casual"},
    {"name": "Oversized Graphic Tee", "brand": "Urban Outfitters", "price": "35.00", "image_url": "https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=500&q=80", "product_url": "https://www.urbanoutfitters.com", "target_shapes": ["Rectangle", "Inverted Triangle", "Apple"], "segment": "Womenswear", "concept": "Casual"},
    {"name": "Cropped Cardigan", "brand": "Aritzia", "price": "110.00", "image_url": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=500&q=80", "product_url": "https://www.aritzia.com", "target_shapes": ["Pear", "Hourglass"], "segment": "Womenswear", "concept": "Casual"},
    
    # WOMENSWEAR - FORMAL
    {"name": "Structured Shoulder Blazer", "brand": "Mango", "price": "119.99", "image_url": "https://images.unsplash.com/photo-1548624149-f9b1859aa7d0?w=500&q=80", "product_url": "https://shop.mango.com", "target_shapes": ["Pear", "Spoon", "Rectangle"], "segment": "Womenswear", "concept": "Formal"},
    {"name": "Deep V-Neck Silk Blouse", "brand": "Massimo Dutti", "price": "95.00", "image_url": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500&q=80", "product_url": "https://www.massimodutti.com", "target_shapes": ["Inverted Triangle", "Apple", "Rectangle"], "segment": "Womenswear", "concept": "Formal"},
    {"name": "Tailored Wide-Leg Trousers", "brand": "Everlane", "price": "128.00", "image_url": "https://images.unsplash.com/photo-1509631179647-0c500ab14c55?w=500&q=80", "product_url": "https://www.everlane.com", "target_shapes": ["Hourglass", "Pear"], "segment": "Womenswear", "concept": "Formal"},
    {"name": "Belted Trench Coat", "brand": "Burberry", "price": "1250.00", "image_url": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=500&q=80", "product_url": "https://www.burberry.com", "target_shapes": ["Hourglass", "Rectangle", "Pear"], "segment": "Womenswear", "concept": "Formal"},
    
    # WOMENSWEAR - STREETWEAR
    {"name": "Parachute Cargo Pants", "brand": "Jaded London", "price": "90.00", "image_url": "https://images.unsplash.com/photo-1617137968427-85924c800a22?w=500&q=80", "product_url": "https://jadedldn.com", "target_shapes": ["Inverted Triangle", "Rectangle", "Apple"], "segment": "Womenswear", "concept": "Streetwear"},
    {"name": "Chunky Platform Sneakers", "brand": "New Balance", "price": "130.00", "image_url": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=500&q=80", "product_url": "https://www.newbalance.com", "target_shapes": ["All"], "segment": "Womenswear", "concept": "Streetwear"},

    # MENSWEAR - CASUAL
    {"name": "Tapered Cargo Joggers", "brand": "Nike", "price": "75.00", "image_url": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500&q=80", "product_url": "https://www.nike.com", "target_shapes": ["Inverted Triangle", "Rectangle", "Athletic"], "segment": "Menswear", "concept": "Casual"},
    {"name": "Classic Relaxed Fit Tee", "brand": "Uniqlo", "price": "19.90", "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&q=80", "product_url": "https://www.uniqlo.com", "target_shapes": ["Apple", "Pear", "Rectangle"], "segment": "Menswear", "concept": "Casual"},
    {"name": "Slim Fit Denim Jeans", "brand": "Diesel", "price": "150.00", "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500&q=80", "product_url": "https://www.diesel.com", "target_shapes": ["Athletic", "Inverted Triangle"], "segment": "Menswear", "concept": "Casual"},
    
    # MENSWEAR - FORMAL
    {"name": "Slim Fit Oxford Shirt", "brand": "Ralph Lauren", "price": "125.00", "image_url": "https://images.unsplash.com/photo-1596755094514-f87e32f85e2c?w=500&q=80", "product_url": "https://www.ralphlauren.com", "target_shapes": ["Athletic", "Inverted Triangle", "Hourglass"], "segment": "Menswear", "concept": "Formal"},
    {"name": "Tailored Wool Suit Jacket", "brand": "SuitSupply", "price": "399.00", "image_url": "https://images.unsplash.com/photo-1594938298598-70f70fc67120?w=500&q=80", "product_url": "https://suitsupply.com", "target_shapes": ["Pear", "Rectangle", "Athletic"], "segment": "Menswear", "concept": "Formal"},
    
    # MENSWEAR - STREETWEAR
    {"name": "Heavyweight Hoodie", "brand": "Carhartt WIP", "price": "118.00", "image_url": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500&q=80", "product_url": "https://www.carhartt-wip.com", "target_shapes": ["Rectangle", "Apple", "Inverted Triangle"], "segment": "Menswear", "concept": "Streetwear"},

    # KIDSWEAR 
    {"name": "Comfort Stretch Overalls", "brand": "OshKosh", "price": "35.00", "image_url": "https://images.unsplash.com/photo-1519238396246-bd6993510e47?w=500&q=80", "product_url": "https://www.oshkosh.com", "target_shapes": ["All"], "segment": "Kidswear", "concept": "Casual"},
    {"name": "Cotton Graphic Tee", "brand": "Gap Kids", "price": "15.00", "image_url": "https://images.unsplash.com/photo-1503919545889-aef636e10ad4?w=500&q=80", "product_url": "https://www.gap.com", "target_shapes": ["All"], "segment": "Kidswear", "concept": "Casual"}
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
        elif req.left_shoulder and req.left_hip:
            shape_result = "Athletic" 
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
            {"name": f"Universal Fit Essential ({req.concept})", "brand": "FitBot Basics", "price": "29.99", "image_url": "https://images.unsplash.com/photo-1620799140188-3b2a02fd9a77?w=500&q=80", "product_url": "https://google.com"}
        ]

    return {"shape": shape_result, "products": recommended_products}
