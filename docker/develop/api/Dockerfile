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

EXPOSE 8050 587

ENTRYPOINT ["gunicorn", "-w 8", "-k gthread", "-b :8050", "-t 60", "--keep-alive", "4", "--reload", "--access-logfile", "-", "--error-logfile",  "-", "wsgi:connexion_app"]