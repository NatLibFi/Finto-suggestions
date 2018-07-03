from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Suggestion(db.Model):
    id = db.Column('suggestion_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Suggestion {}>'.format(self.name)
