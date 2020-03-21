
from typing import List

import pandas as pd
import pybreaker
import uvicorn
from fastapi import Depends, FastAPI
from numpy import random
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


@app.post("/ads", response_model=List[schemas.Product])
def getAds(db: Session = Depends(get_db)):
    skip = 500
    some_products = set(crud.get_products(db, skip=skip, limit=1000))
    print(some_products)
    return list(some_products)[0:10]


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)