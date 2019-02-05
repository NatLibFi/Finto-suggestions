import requests
import time,sys

from app import create_app
from api.models import db

from .github_data_parser import GithubDataParser
from .db_inserter import DBInserter


if __name__ == '__main__':
  print("Starting production data importer...")
  app = create_app()
  db.app = app.app
  parser = GithubDataParser()
  print("Handling Github issue fetch and parsing the responses to models...")
  models = parser.handle_response()
  print("Models to handle: ", len(models))
  print("Map models data to db business objects and insert data to database")
  db_importer = DBInserter()
  db_importer.insert_models_to_db(db, models)
