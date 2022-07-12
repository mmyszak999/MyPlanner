FROM python:3.9.6-slim-buster

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt \
    && apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]