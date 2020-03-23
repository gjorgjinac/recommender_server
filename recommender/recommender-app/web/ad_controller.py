import json
from typing import List

import pybreaker
import requests
from fastapi import APIRouter

from default_ad_listener import DefaultListener
from defaults import default_ads
from helper import call_protected
from repository import schemas

ad_router = APIRouter()

ad_circuit_breaker = pybreaker.CircuitBreaker(
    fail_max=1, listeners=[DefaultListener()],
    reset_timeout=10,
)

@ad_circuit_breaker
def send_post_for_adds():
    print('requesting')
    response = requests.post("http://127.0.0.1:8001/ads")
    return json.loads(response.text)

@ad_circuit_breaker
def sabotage_ad():
    raise Exception

@ad_router.get("/ads", response_model=List[schemas.Product])
async def get_ads():
    return call_protected(ad_circuit_breaker, default_ads, send_post_for_adds)