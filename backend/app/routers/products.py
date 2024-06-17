from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.dependencies import get_user_from_session
import os
from uuid import uuid4
from datetime import datetime
from app.models import User, Session, Product, Category
from app.config import SessionLocal


router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Route not found"}},
)

# Create Product
class CreateProductRequest(BaseModel):
    name: str
    category_id: int
    price: float
    desc: str
    features: dict

@router.post("/")
async def create_product(request: CreateProductRequest, user: User = Depends(get_user_from_session)):
    with SessionLocal() as db:
        # Check if user is admin
        if not user['is_admin']:
            return JSONResponse(status_code=403, content={"message": "Unauthorized"})
        
        # make sure features is a dictionary that has all the required keys for the category's config_params
        category = db.query(Category).filter(Category.id == request.category_id).first()

        if category is None:
            return JSONResponse(status_code=404, content={"message": "Category not found"})
        
        required_keys = category.config_params.split(", ")
        for key in required_keys:
            if key not in request.features:
                return JSONResponse(status_code=400, content={"message": f"Missing key in features: {key}"})

        # Create product
        product = Product(
            name=request.name,
            category_id=request.category_id,
            price=request.price,
            desc=request.desc,
            features=str(request.features),
            rating=0.0
        )
        db.add(product)
        db.commit()
        return product
    

# Get Products
@router.get("/")
async def get_products():
    with SessionLocal() as db:
        products = db.query(Product).all()
        return products
    

# recommendaion - best rated given price and category
@router.get("/recommendation")
async def get_recommendation(category_id: int, price: float):
    with SessionLocal() as db:
        products = db.query(Product).filter(Product.category_id == category_id, Product.price <= price).all()
        products = sorted(products, key=lambda x: x.rating, reverse=True)
        return products

# Get Product by ID
@router.get("/{product_id}")
async def get_product(product_id: int):
    with SessionLocal() as db:
        product = db.query(Product).filter(Product.id == product_id).first()
        return product