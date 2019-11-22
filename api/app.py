import os
import connexion
import click
from datetime import timedelta
from flask_migrate import Migrate
from flask.cli import with_appcontext
from flask_cors import CORS
from specsynthase.specbuilder import SpecBuilder
from api.models import *
from api.authentication import jwt, prune_expired_tokens
#
import json
# from flask import json
from flask.json import JSONEncoder
import logging
# import ujson


# Here you can adjust error logging levels
# logging.basicConfig()   # log messages to stdout
# logging.getLogger('sqlalchemy.dialects.postgresql').setLevel(logging.DEBUG)

# psycopg2.extras.register_default_json(globally=True, loads=loads)
# conn = psycopg2.connect(...)
# psycopg2.extras.register_default_json(conn, loads=loads)


# def create_app(config_object='config.DevelopmentConfig'):
def create_app(config_object='config.DevelopmentConfig'):

    app = connexion.FlaskApp(__name__, specification_dir='api/specification/')
    # app

    # This is required for Flask CLI and FLASK_APP env to work
    flask_app = app.app
    # flask_app.json.JSONEncoder(ensure_ascii=False)

    flask_app.secret_key = os.environ.get('APP_SECRET_KEY')
    flask_app.config.from_object(config_object)

    # Specsynthase's SpecBuilder combines multiple Swagger yaml files into a one.
    # This is purely used for modularity.
    # https://github.com/zalando/connexion/issues/254
    api_spec = _build_swagger_spec(SpecBuilder())


    # In case you don't want to show the swagger_ui for private endpoints
    # You might want to split this into two apis
    enable_swagger = flask_app.config['ENABLE_SWAGGER_UI']
    app.add_api(api_spec, options={"swagger_ui": enable_swagger})


    db.init_app(flask_app)
    # flask_app.OPTIONS.psycopg2.register_default_json.
    jwt.init_app(flask_app)
    migrate = Migrate(flask_app, db, compare_type=True)

    # CORS settings for allowing suggestions from a Skosmos client
    CORS(flask_app, resources={r"/api/suggestions": {
        "origins": os.environ.get('SKOSMOS_URI'),
        "allow_headers": ['Content-Type', 'Access-Control-Allow-Origin'],
        "methods": ['POST', 'OPTIONS']
    }})

    @flask_app.shell_context_processor
    def shell_context():
        import api.models as models
        from pprint import pprint
        return {
            'app': app,
            'db': models.db,
            'pprint': pprint,
            'models': models
        }
        # models.db.

    @flask_app.cli.command(db.JSON)
    def prune():
        """
        Prunes the JWT token blacklist.

        Run this from command line (or periodically from crontab, for example)
        >> flask prune
        """

        no_pruned = prune_expired_tokens()
        click.echo(
            '{} expired tokens pruned from the database.'.format(no_pruned))

    @flask_app.cli.command()
    # def json_testing();


    @click.argument('name')
    @click.argument('email')
    @click.argument('password')
    def create_admin(name, email, password):
        """
        Creates an admin user

        Run this from command line
        >> flask create_admin
        """

        user = User(name=name,
                    email=email,
                    password=password,
                    role=UserRoles.ADMIN)
        db.session.add(user)
        db.session.commit()

        click.echo('Created admin user {}.'.format(email))

    return app


def _build_swagger_spec(builder):
    # Common
    builder.add_spec('api/specification/api.yaml')
    builder.add_spec('api/specification/definitions.yaml')
    builder.add_spec('api/specification/authentication.yaml')

    # API Endpoints
    builder.add_spec('api/specification/events.yaml')
    builder.add_spec('api/specification/meetings.yaml')
    builder.add_spec('api/specification/reactions.yaml')
    builder.add_spec('api/specification/suggestions.yaml')
    builder.add_spec('api/specification/tags.yaml')
    builder.add_spec('api/specification/users.yaml')

    return builder


if __name__ == '__main__':
    app = create_app('config.DevelopmentConfig')
    # app.register_default_json(loads=ujson.loads, globally=True)
    # app.register_default_jsonb(loads=ujson.loads, globally=True)
    app.run(host='0.0.0.0', port=8050, debug=True)
