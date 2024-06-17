from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.dependencies import get_user_from_session
import os
from uuid import uuid4
from datetime import datetime
from app.models import User, Session, Category
from app.config import SessionLocal


router = APIRouter(
    prefix="/category",
    tags=["category"],
    responses={404: {"description": "Route not found"}},
)


# Get Categories
@router.get("/")
async def get_categories():
    with SessionLocal() as db:
        categories = db.query(Category).all()
        return categories

# Get Categories by ID
@router.get("/{category_id}")
async def get_category(category_id: int):
    with SessionLocal() as db:
        category = db.query(Category).filter(Category.id == category_id).first()
        return category