FROM python:3-alpine

ENV PYTHONUNBUFFERED 1

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

ENTRYPOINT ["gunicorn", "-w", "2", "-b", ":8050", "--reload", "--access-logfile", "-", "--error-logfile", "-", "wsgi:connexion_app"]
