import ast
import json
from typing import List

import pandas as pd
import pybreaker
import requests
import uvicorn
from fastapi import Depends, FastAPI
from repository import models, crud, schemas
from repository.database import SessionLocal, engine
from repository.models import Review
from sqlalchemy.orm import Session

from code.recommender.default_ad_listener import DefaultAdListener

models.Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/products/{asin}", response_model=schemas.Product)
async def get_product(asin, db: Session = Depends(get_db)):
    return crud.get_product_by_asin(db, asin)


@app.get("/products", response_model=List[schemas.Product])
async def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


@app.get("/writeProducts")
async def writeProducts(db: Session = Depends(get_db)):
    products = pd.read_csv('repository/data/meta_office.csv', index_col=[0])
    products.to_sql('products', con=engine, if_exists='append', index=False)


@app.get("/writeReviews")
async def writeReviews(db: Session = Depends(get_db)):
    reviews = pd.read_csv('repository/data/office_both_set.csv', index_col=[0])
    existing_reviews = set(['{0}_{1}'.format(review.reviewerID, review.asin) for review in crud.get_reviews(db)])
    for index, row in reviews.iterrows():
        if not '{0}_{1}'.format(row['reviewerID'], row['asin']) in existing_reviews:
            crud.create_review(db, row)
            print(row['asin'])


@app.get("/products/{asin}/reviews")
async def getReviewForProduct(asin, db: Session = Depends(get_db)) -> List[Review]:
    return crud.get_reviews_by_asin(db, asin)


@app.get("/reviews", response_model=List[schemas.Review])
async def get_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_reviews(db, skip=skip, limit=limit)


@app.post("/reviews", response_model=schemas.Review)
async def create_review(review: schemas.Review, db: Session = Depends(get_db)):
    return crud.create_review(db, review)


ad_circuit_breaker = pybreaker.CircuitBreaker(
    fail_max=1, listeners=[DefaultAdListener()],
    reset_timeout=10,
)

@ad_circuit_breaker
def send_post_for_adds():
    print('requesting')
    response = requests.post("http://127.0.0.1:8001/ads")
    return json.loads(response.text)


@app.get("/ads", response_model=List[schemas.Product])
async def get_ads(db: Session = Depends(get_db)):
    default_ads = [crud.get_product_by_asin(db, 'B00000JBLH')]
    return call_protected(ad_circuit_breaker, send_post_for_adds, default_ads)

def call_protected(circuit_breaker, protected_function, default_data):
    try:
        data = protected_function()
    except Exception:
        pass
    if circuit_breaker.current_state == 'open':
        print('defaulting')
        data = default_data
    print(data)
    return data

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
