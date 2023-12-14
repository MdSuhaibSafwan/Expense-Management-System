FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# System Deps
RUN pip install "poetry==1.7"

# Cache Only Requirements To Cache Them In Docker Layer
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# Project Initialization
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$ENV_ARG" == production && echo "--no-dev") --no-interaction --no-ansi

# Coping Folders and Files For Project
COPY . /app/
RUN sed -i 's/\r$//g' /app/deployment/*
RUN chmod +x /app/deployment/*

ENTRYPOINT ["/app/deployment/entrypoint"]
