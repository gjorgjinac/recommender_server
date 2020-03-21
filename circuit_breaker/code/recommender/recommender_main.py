import uvicorn
from fastapi import Depends, FastAPI
from repository import models
from repository.database import engine
from repository.database import get_db

from code.recommender.web.ad_controller import ad_router
from code.recommender.web.product_controller import product_router
from code.recommender.web.review_controller import review_router
from code.recommender.web.sabotage_controller import sabotage_router

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


app.include_router(
    product_router,
    tags=["products"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    review_router,
    tags=["reviews"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)


app.include_router(
    ad_router,
    tags=["ads"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    sabotage_router
)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
