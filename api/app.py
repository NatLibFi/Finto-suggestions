import connexion
from api.models import db

# Create a WSGI compliant app instance
cx_app = connexion.FlaskApp(__name__, specification_dir='api/specification/')

# Add PSQL database config for SQLAlchemy
connection_string_template = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'
connection_string = connection_string_template.format(
    user='psql',
    passwd='pw',
    host='db',
    port='5432',
    db='psdb')

cx_app.app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
cx_app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cx_app.app.secret_key = 'foobarbaz'  # TODO: change

# Init database models
db.init_app(cx_app.app)

# Add Connexion API endpoints
cx_app.add_api('suggestion.yaml', base_path="/api/v1")

if __name__ == "__main__":
    cx_app.run(host="0.0.0.0", port=8050, debug=True)
