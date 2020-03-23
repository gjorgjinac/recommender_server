from typing import List

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from repository import database

from repository import schemas, crud

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


@app.post("/ads", response_model=List[schemas.Product])
def getAds(db: Session = Depends(database.get_db)):
    skip = 500
    some_products = set(crud.get_products(db, skip=skip, limit=1000))
    print(some_products)
    return list(some_products)[0:10]


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)