FROM python:3.8-slim

COPY ./src /src

RUN pip install -r /src/requirements.txt
