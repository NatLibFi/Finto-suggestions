import connexion
import os
from api.models import db

# Create a WSGI compliant app instance
app = connexion.FlaskApp(__name__, specification_dir='api/specification/')

# This is required for Flask cli and FLASK_APP env to work
flask_app = app.app

# Add PSQL database config for SQLAlchemy
flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')

# http://flask-sqlalchemy.pocoo.org/2.1/signals/
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

flask_app.secret_key = os.environ.get('APP_SECRET_KEY')

# Init database models
db.init_app(flask_app)

# Add Connexion API endpoints
app.add_api('suggestion.yaml', base_path="/api/v1")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
