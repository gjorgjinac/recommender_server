from typing import List

import pandas as pd
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from defaults import default_products, default_reviews
from helper import call_protected
from repository import crud, schemas
from repository.crud import db_circuit_breaker
from repository.database import engine, get_db
from repository.models import Review

product_router = APIRouter()


@product_router.get("/products/{asin}", response_model=schemas.Product)
async def get_product(asin, db: Session = Depends(get_db)):
    return call_protected(db_circuit_breaker, default_products[0], crud.get_product_by_asin,  db, asin)


@product_router.get("/products", response_model=List[schemas.Product])
async def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return call_protected(db_circuit_breaker, default_products, crud.get_products,  db, skip,limit)


@product_router.get("/writeProducts")
async def writeProducts(db: Session = Depends(get_db)):
    products = pd.read_csv('repository/data/meta_office.csv', index_col=[0])
    products.to_sql('products', con=engine, if_exists='append', index=False)


@product_router.get("/products/{asin}/reviews")
async def getReviewForProduct(asin, db: Session = Depends(get_db)) -> List[Review]:
    return call_protected(db_circuit_breaker, default_reviews, crud.get_product_by_asin, db, asin)
