import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

# Simple products endpoint for the shop
@app.get("/api/products")
def get_products():
    return [
        {
            "id": 1,
            "title": "Premium Attar",
            "description": "Long-lasting fragrance oil.",
            "price": 15.99,
            "category": "fragrance",
            "image": "https://images.unsplash.com/photo-1590152561800-7183d3d3b28e?q=80&w=600&auto=format&fit=crop"
        },
        {
            "id": 2,
            "title": "Classic Blue Jeans",
            "description": "Comfort fit denim jeans.",
            "price": 39.99,
            "category": "clothing",
            "image": "https://images.unsplash.com/photo-1516826957135-700dedea698c?q=80&w=600&auto=format&fit=crop"
        },
        {
            "id": 3,
            "title": "Stainless Water Bottle",
            "description": "Insulated bottle keeps drinks cold/hot.",
            "price": 18.5,
            "category": "accessories",
            "image": "https://images.unsplash.com/photo-1561214115-f2f134cc4912?q=80&w=600&auto=format&fit=crop"
        },
        {
            "id": 4,
            "title": "Travel Backpack",
            "description": "Durable bag with multiple compartments.",
            "price": 49.0,
            "category": "bags",
            "image": "https://images.unsplash.com/photo-1504274066651-8d31a536b11a?q=80&w=600&auto=format&fit=crop"
        }
    ]

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
