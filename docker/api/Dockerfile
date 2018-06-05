FROM python:3-alpine

ENV PYTHONUNBUFFERED 1

COPY ./api /app
WORKDIR /app

# Manage dependencies using pipenv
RUN pip install pipenv \
  && pipenv install --system

EXPOSE 8050

# CMD ["python", "app.py"]
CMD ["gunicorn", "-w", "2", "-b", ":8050", "--reload", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
