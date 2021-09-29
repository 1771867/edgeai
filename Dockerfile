FROM python:3.7-slim-buster

RUN mkdir /boosting

WORKDIR /boosting

COPY . .

RUN pip install -r BoostingClassifier/requirements.txt

EXPOSE 9007

CMD ["python", "BoostingClassifier/waitress_server.py"]



