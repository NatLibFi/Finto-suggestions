from app import flask_app, db

with flask_app.app_context():
    db.create_all()

print("Database initialized.")
