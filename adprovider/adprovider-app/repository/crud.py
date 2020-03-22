from typing import List

from sqlalchemy.orm import Session

from . import models, schemas


def get_product_by_asin(db: Session, asin: str):
    return db.query(models.Product).filter(models.Product.asin == asin).first()

def get_products(db: Session, skip: int = 0, limit: int = None) -> List[models.Product]:
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, new_product:any):
    db_product = models.Product(**new_product.to_dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_reviews_by_asin(db: Session, asin: str) -> List[models.Review]:
    return db.query(models.Review).filter(models.Review.asin == asin).all()

def get_reviews(db: Session, skip: int = 0, limit: int = None) -> List[models.Review]:
    return db.query(models.Review).offset(skip).limit(limit).all()


def create_review(db: Session, new_review: schemas.ReviewBase) -> models.Review:
    product = get_product_by_asin(db, new_review.asin)
    db_review = models.Review(**new_review.to_dict(), product_id = product.id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

