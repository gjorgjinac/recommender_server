FROM python:3
MAINTAINER Gjorgjina Cenikj "gjorgjinac@gmail.com"
COPY ./adprovider-app /adprovider
RUN apt-get update -y && apt-get install -y python-pip python-dev
COPY ./requirements.txt /adprovider/requirements.txt
WORKDIR /adprovider
RUN pip3 install -r requirements.txt
COPY . /adprovider
ENTRYPOINT [ "python" ]
EXPOSE 5000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "5000", "adprovider_main:app"]