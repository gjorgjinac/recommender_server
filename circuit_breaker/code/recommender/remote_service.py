import pandas as pd

from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from repository import models, database, crud, schemas
from repository.database import SessionLocal, engine

from repository.models import Review

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



@app.get("/products/{asin}")
async def get_product(asin, db: Session = Depends(get_db)):
    return crud.get_product(db, asin)

@app.get("/products", response_model=dict)
async def get_products(skip: int = 0, limit: int = 1, db: Session = Depends(get_db)):
    return {'products': crud.get_products(db, skip=skip, limit=limit)}

@app.get("/writeProducts")
async def writeProducts(db: Session = Depends(get_db)):
    products = pd.read_csv('repository/data/meta_office.csv', index_col=[0])
    existing_products = set([product.asin for product in crud.get_products(db)])
    print(products.shape)
    print(len(existing_products))
    for index, row in products.iterrows():
        if not row['asin'] in existing_products:
            crud.create_product(db,row)
            print(row['asin'])

@app.get("/writeReviews")
async def writeReports(db: Session = Depends(get_db)):
    reviews = pd.read_csv('repository/data/office_both_set.csv', index_col=[0])
    existing_reviews = set(['{0}_{1}'.format(review.reviewerID, review.asin) for review in crud.get_reviews(db)])
    for index, row in reviews.iterrows():
        if not '{0}_{1}'.format(row['reviewerID'], row['asin']) in existing_reviews:
            crud.create_review(db,row)
            print(row['asin'])

@app.get("/products/{asin}/reviews")
async def getReviewForProduct(asin, db:Session = Depends(get_db)) -> List[Review]:
    return crud.get_reviews_by_asin(db,asin)

@app.get("/reviews", response_model=dict)
async def get_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return {'reviews': crud.get_reviews(db, skip=skip, limit=limit)}