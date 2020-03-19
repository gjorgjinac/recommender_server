from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Text
from sqlalchemy.orm import relationship

from .database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    asin = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    imUrl = Column(String)
    related = Column(Text)
    salesRank = Column(String)
    categories = Column(String)
    brand = Column(String)
    price = Column(Float)
    reviews = relationship("Review", back_populates="product")



class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="reviews")

    reviewerID = Column(String)
    asin = Column(String)
    reviewerName = Column(String)
    helpful = Column(String)
    reviewText = Column(Text)
    overall = Column(Integer)
    summary = Column(Text)
    unixReviewTime = Column(String)
    reviewTime = Column(String)
