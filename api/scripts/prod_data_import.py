import requests, time, sys

from app import create_app
from api.models import db

from .github_data_parser import GithubDataParser
from .db_inserter import DBInserter

def parse_args():
  args = sys.argv
  if args is not None and len(args) > 0:
    for arg in args:
      if 'loop-count' in arg:
        return int(arg.split('loop-count=')[1].strip())
  return None

if __name__ == '__main__':
  print("Starting production data importer...")
  app = create_app()
  db.app = app.app
  parser = GithubDataParser()
  print("Handling Github issue fetch and parsing the responses to models...")

  arg_loop_count = parse_args()
  models = parser.handle_response(arg_loop_count)
  print("Models to handle: ", len(models))
  print("Map models data to db business objects and insert data to database")
  db_importer = DBInserter(db)
  db_importer.insert_models_to_db(db, models)
