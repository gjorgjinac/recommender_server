import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .db_creds import user,password,dbname

#SQLALCHEMY_DATABASE_URL = "postgresql://{user}:{password}@localhost:5432/{dbname}".format(user=user,password=password,dbname=dbname)
SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URI')
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()