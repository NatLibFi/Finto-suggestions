FROM python:3-alpine

ENV PYTHONUNBUFFERED 1
ENV APP_CONFIG_OBJECT=config.TestingConfig

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

# ENTRYPOINT ["gunicorn", "--bind", ":8050", "--log-level=DEBUG", "-", "--access-logfile", "-", "--error-logfile", "-", "wsgi:connexion_app"]
ENTRYPOINT ["gunicorn", "--bind", ":8050", "--access-logfile", "-", "--error-logfile", "-", "wsgi:connexion_app"]