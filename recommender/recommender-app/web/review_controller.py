from typing import List

import pandas as pd
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from code.recommender.defaults import default_reviews
from code.recommender.helper import call_protected
from code.recommender.repository import crud, schemas
from code.recommender.repository.crud import db_circuit_breaker
from code.recommender.repository.database import engine, get_db

review_router = APIRouter()
@review_router.get("/reviews", response_model=List[schemas.Review])
async def get_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return call_protected(db_circuit_breaker,default_reviews,crud.get_reviews, db, skip, limit)


@review_router.post("/reviews", response_model=schemas.Review)
async def create_review(review: schemas.Review, db: Session = Depends(get_db)):
    return crud.create_review(db, review)


@review_router.get("/writeReviews")
async def writeReviews(db: Session = Depends(get_db)):
    reviews = pd.read_csv('repository/data/office_both_set.csv', index_col=[0])
    existing_reviews = set(['{0}_{1}'.format(review.reviewerID, review.asin) for review in crud.get_reviews(db)])
    for index, row in reviews.iterrows():
        if not '{0}_{1}'.format(row['reviewerID'], row['asin']) in existing_reviews:
            crud.create_review(db, row)
            print(row['asin'])