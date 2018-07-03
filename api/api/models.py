from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Suggestion {}>'.format(self.name)
