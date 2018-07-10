import connexion
import os
from api.models import db, User, Suggestion, Event, Meeting, Emoji, Tag, EventType
from flask_migrate import Migrate

# Create a WSGI compliant Connexion app instance and initialize the API
app = connexion.FlaskApp(__name__, specification_dir='api/specification/')
app.add_api('suggestion.yaml', base_path="/api/v1")

# This is required for Flask cli and FLASK_APP env to work
flask_app = app.app

# Add PSQL database config for SQLAlchemy
flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
# Disable signals. http://flask-sqlalchemy.pocoo.org/2.1/signals/
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

flask_app.secret_key = os.environ.get('APP_SECRET_KEY')

# Init database models and migrations
db.init_app(flask_app)
migrate = Migrate(flask_app, db)


@flask_app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Suggestion': Suggestion,
        'Event': Event,
        'Meeting': Meeting,
        'Emoji': Emoji,
        'Tag': Tag,
        'EventType': EventType
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
