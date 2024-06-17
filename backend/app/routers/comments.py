from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.dependencies import get_user_from_session
import os
from uuid import uuid4
from datetime import datetime
from app.models import User, Session, Product, Category, Comment
from app.config import SessionLocal


router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"description": "Route not found"}},
)


# Create Comment
class CreateCommentRequest(BaseModel):
    product_id: int
    rating: dict
    body: str

@router.post("/")
async def create_comment(request: CreateCommentRequest, user: User = Depends(get_user_from_session)):
    with SessionLocal() as db:
        # Check if user is admin
        if user is None:
            return JSONResponse(status_code=403, content={"message": "Unauthorized"})
        
        # make sure rating is a dictionary that has all the required keys for the product's category's rating_params
        product = db.query(Product).filter(Product.id == request.product_id).first()

        if product is None:
            return JSONResponse(status_code=404, content={"message": "Product not found"})
        
        category = db.query(Category).filter(Category.id == product.category_id).first()
        required_keys = category.rating_params.split(", ")
        for key in required_keys:
            if key not in request.rating:
                return JSONResponse(status_code=400, content={"message": f"Missing key in rating: {key}"})

        # Create comment
        comment = Comment(
            product_id=request.product_id,
            user_id=user['id'],
            rating=str(request.rating),
            body=request.body
        )
        db.add(comment)

        # Update product rating based on the new comment
        new_rating_total = 0
        new_rating_cnt = 0
        for key in request.rating:
            new_rating_total += float(request.rating[key])
            new_rating_cnt += 1
        new_rating = new_rating_total / new_rating_cnt

        # total comment count of the product
        comment_count = db.query(Comment).filter(Comment.product_id == request.product_id).count()

        # current rating of the product
        current_rating = product.rating

        # new rating of the product
        new_rating = (current_rating * comment_count + new_rating) / (comment_count + 1)

        product.rating = new_rating

        # round to 2 decimal places
        product.rating = round(product.rating, 2)

        db.commit()
        return comment
    

# List comment of a product
@router.get("/{product_id}")
async def list_comment(product_id: int):
    with SessionLocal() as db:
        comments = db.query(Comment).filter(Comment.product_id == product_id).all()
        return comments