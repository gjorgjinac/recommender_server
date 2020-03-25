### Intro
This application is made out of two services, **recommender** and **ad_provider** service. Ad_provider has two circuit breakers: one for the providing ads for the **recommender** service and one for the database, in this case PostgreSQL.

### Docker setup
In order to run this project:
```sh
$ git clone https://github.com/gjorgjinac/recommender_server.git
$ cd recommender_server
$ docker-compose up
```
This will run the two, beforementioned, services. Verification of the deployment can be done by navigating to the following server addresses in your preferred browser:
```sh
0.0.0.0:8000 #for the recommended service
0.0.0.0:8001 #for the ad_provider service
```
![alt text](https://i.imgur.com/y3XiMDg.png)
### Configuration
The configuration on the PyBreaker for the `/ads` breaker which protects calls to `0.0.0.0:8000/ads`.
```python
ad_circuit_breaker = pybreaker.CircuitBreaker( 
    fail_max=1, listeners=[DefaultListener()],
    reset_timeout=10,
)
```
where the `DefaultListener()` can be found in `recommender/recommender-app/default_ad_listener.py`.

On the other side, the configuration on the PyBreaker which protects calls to the database.
```python
db_circuit_breaker = pybreaker.CircuitBreaker(
    fail_max=1,
    reset_timeout=20,
)
```
### Test cases for the circuit breakers
1. Circuit breaker which protects the calls from the recommender service to ad_provider service: execute a GET request to `http://0.0.0.0:8000/ads`.
```python
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
```
![alt text](https://i.imgur.com/TbCllQs.png)
2. Circuit breaker meant to protect the calls from the recommender service to the operational database with content type application/json and with body

![alt text](https://i.imgur.com/sQhi54U.png)
```python
db_circuit_breaker = pybreaker.CircuitBreaker(
    fail_max=1,
    reset_timeout=20,
)

@db_circuit_breaker
def get_product_by_asin(db: Session, asin: str):
    return db.query(models.Product).filter(models.Product.asin == asin).first()

@db_circuit_breaker
def get_products(db: Session, skip: int = 0, limit: int = None) -> List[models.Product]:
    return db.query(models.Product).offset(skip).limit(limit).all()

@db_circuit_breaker
def create_product(db: Session, new_product:any):
    db_product = models.Product(**new_product.to_dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@db_circuit_breaker
def get_reviews_by_asin(db: Session, asin: str) -> List[models.Review]:
    return db.query(models.Review).filter(models.Review.asin == asin).all()

@db_circuit_breaker
def get_reviews(db: Session, skip: int = 0, limit: int = None) -> List[models.Review]:
    return db.query(models.Review).offset(skip).limit(limit).all()

@db_circuit_breaker
def create_review(db: Session, new_review: schemas.ReviewBase) -> models.Review:
    product = get_product_by_asin(db, new_review.asin)
    db_review = models.Review(**new_review.to_dict(), product_id = product.id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@db_circuit_breaker
def fail():
    raise Exception
```
