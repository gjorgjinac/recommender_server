from fastapi import APIRouter

from code.recommender.repository import crud
from code.recommender.web.ad_controller import sabotage_ad

sabotage_router = APIRouter()

@sabotage_router.get('/sabotage-db')
async def sabotage_db():
    print('sabotage db')
    crud.fail()

@sabotage_router.get('/sabotage-ad-server')
async def sabotage_ad_server():
    print('sabotage_ad_sever')
    sabotage_ad()