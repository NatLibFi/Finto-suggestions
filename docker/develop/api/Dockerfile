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

# Intall and register frdlib-jsonld
# EXTRA 
RUN pip install --upgrade pip
RUN pip install rdflib-jsonld

# Manage dependencies using pipenv
RUN pip install pipenv \
  && pipenv lock --clear \
  && pipenv lock -r \
  && pipenv install --deploy --system
  
  #Testing

EXPOSE 8050 587

ENTRYPOINT ["gunicorn", "--config", "gunicorn_config_dev.conf", "wsgi:connexion_app"]
