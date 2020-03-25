FROM python:3
MAINTAINER Gjorgjina Cenikj "gjorgjinac@gmail.com"
COPY ./recommender-app /recommender
RUN apt-get update -y && apt-get install -y python-pip python-dev
COPY ./requirements.txt /recommender/requirements.txt

WORKDIR /recommender

RUN pip3 install -r requirements.txt

COPY . /recommender/

CMD uvicorn recommender-app.recommender_main:app --reload --host 0.0.0.0 --port 8000