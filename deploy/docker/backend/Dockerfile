FROM python:3.12-slim-bookworm AS build

ARG DJANGO_ENV=development
ENV DJANGO_ENV=${DJANGO_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.3 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/var/cache/pypoetry

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
       bash build-essential curl gettext git libpq-dev wget \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip \
    && pip install "poetry==${POETRY_VERSION}" \
    && poetry --version

WORKDIR /src
COPY pyproject.toml poetry.lock /src/
RUN poetry install
COPY /src .
