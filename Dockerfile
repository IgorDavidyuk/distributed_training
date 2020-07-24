FROM python:3.6-slim

RUN python -m pip install --upgrade pip && python -m pip install pipenv

WORKDIR /usr/src/app
COPY ./Pipfile ./
COPY ./.env ./
RUN pipenv install

COPY ./prepare_data.py ./
RUN pipenv run python ./prepare_data.py
