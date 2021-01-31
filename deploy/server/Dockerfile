FROM python:3.8-slim

WORKDIR /app/src/
ADD ./server/src/requirements.txt /app/src/

RUN apt-get update && apt-get install gcc build-essential libpq-dev -y && \
    python3 -m pip install --no-cache-dir pip-tools && \
    pip install -r requirements.txt
