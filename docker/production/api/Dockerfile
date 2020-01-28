#FROM python:3.6-alpine
FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1
ENV TZ "Europe/Helsinki"

COPY ./api /app
WORKDIR /app

# This layer is needed for python postgres support
RUN apk update \
  && apk --no-cache add py3-psycopg2 \
  && apk add libpq postgresql-dev \
  && apk add build-base

# Manage dependencies using pipenv
RUN pip install pipenv \
  && pipenv install --system

EXPOSE 8050

ENTRYPOINT ["gunicorn", "--config", "gunicorn_config_production.conf", "wsgi:connexion_app"]