from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.config import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    expires = Column(Float, nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Integer, nullable=False, default=0)

    comments = relationship("Comment", back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    rating_params = Column(String, nullable=False) # csv
    config_params = Column(String, nullable=False) # csv

    products = relationship("Product", back_populates="category")
    


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    price = Column(Float, nullable=False)
    desc = Column(String, nullable=False)
    features = Column(String, nullable=False) # json - from - category's config_params
    rating = Column(Float, nullable=False)

    category = relationship("Category", back_populates="products")
    comments = relationship("Comment", back_populates="product")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(String, nullable=False) # JSON - fron - category's rating_params
    body = Column(String, nullable=False)
    published = Column(Integer, nullable=False, default=1)

    product = relationship("Product", back_populates="comments")
    user = relationship("User", back_populates="comments")

