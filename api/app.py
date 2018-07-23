import connexion
import os
import click
from datetime import timedelta
from api.models import *
from api.authentication import jwt, prune_expired_tokens
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from specsynthase.specbuilder import SpecBuilder

app = connexion.FlaskApp(__name__, specification_dir='api/specification/')

# Specsynthase combines multiple Swagger yaml files into a one.
# This is purely used for modularity.
# https://github.com/zalando/connexion/issues/254
api_spec = SpecBuilder()

# Common
api_spec.add_spec('api/specification/api.yaml')
api_spec.add_spec('api/specification/definitions.yaml')
api_spec.add_spec('api/specification/authentication.yaml')

# API Endpoints
api_spec.add_spec('api/specification/events.yaml')
api_spec.add_spec('api/specification/meetings.yaml')
api_spec.add_spec('api/specification/reactions.yaml')
api_spec.add_spec('api/specification/suggestions.yaml')
api_spec.add_spec('api/specification/tags.yaml')
api_spec.add_spec('api/specification/users.yaml')

# In case you don't want to show the swagger_ui for private endpoints
# You might want to split this into two apis
app.add_api(api_spec, swagger_ui=True)

# This is required for Flask CLI and FLASK_APP env to work
flask_app = app.app

flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
# Disable signals. http://flask-sqlalchemy.pocoo.org/2.1/signals/
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.secret_key = os.environ.get('APP_SECRET_KEY')
flask_app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
flask_app.config['JWT_BLACKLIST_ENABLED'] = True

db.init_app(flask_app)
jwt.init_app(flask_app)

migrate = Migrate(flask_app, db)


@flask_app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Suggestion': Suggestion,
        'Event': Event,
        'Meeting': Meeting,
        'Reaction': Reaction,
        'Tag': Tag,
        'EventTypes': EventTypes,
        'SuggestionStatusTypes': SuggestionStatusTypes,
        'SuggestionTypes': SuggestionTypes,
        'TokenBlacklist': TokenBlacklist
    }


@flask_app.cli.command()
def prune():
    """
    Prunes the JWT token blacklist.

    Run this from command line
    >> flask prune_blacklist
    """

    no_pruned = prune_expired_tokens()
    click.echo('{} expired tokens pruned from the database.'.format(no_pruned))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
