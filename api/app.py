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


def create_app(config_object='config.DevelopmentConfig'):
    app = connexion.FlaskApp(__name__, specification_dir='api/specification/')

    # This is required for Flask CLI and FLASK_APP env to work
    flask_app = app.app

    flask_app.secret_key = os.environ.get('APP_SECRET_KEY')
    flask_app.config.from_object(config_object)

    # Specsynthase's SpecBuilder combines multiple Swagger yaml files into a one.
    # This is purely used for modularity.
    # https://github.com/zalando/connexion/issues/254
    api_spec = _build_swagger_spec(SpecBuilder())

    # In case you don't want to show the swagger_ui for private endpoints
    # You might want to split this into two apis
    enable_swagger = flask_app.config['ENABLE_SWAGGER_UI']
    # TODO: disabled for now, needs fix later on
    app.add_api(api_spec, options={"swagger_ui": False})

    db.init_app(flask_app)
    jwt.init_app(flask_app)
    migrate = Migrate(flask_app, db)

    cors_origins = flask_app.config['CORS_ALLOWED_ORIGINS']

    # only allow CORS for suggestions endpoint
    CORS(flask_app, origins=cors_origins, resources=r"/api/suggestions/*")

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

    @flask_app.cli.command()
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
    app.run(host='0.0.0.0', port=8050, debug=True)
