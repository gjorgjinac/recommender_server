from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .db_creds import user,password,dbname

SQLALCHEMY_DATABASE_URL = "postgresql://{user}:{password}@localhost:5432/{dbname}".format(user=user,password=password,dbname=dbname)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()