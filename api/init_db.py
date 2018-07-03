from app import cx_app, db

with cx_app.app.app_context():
    db.create_all()
