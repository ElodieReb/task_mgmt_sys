# import os
# from flask import Flask
# from flask_migrate import Migrate

# def create_app(test_config=None):
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         SECRET_KEY='dev',
#         SQLALCHEMY_TRACK_MODIFICATIONS=False,
#         SQLALCHEMY_ECHO=True
#     )

#     if test_config is None:
#         # Load the default config when not testing
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         # Load the test config if passed in
#         app.config.from_mapping(test_config)

#     # Ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass

#     # Set up the database
#     from .models import db
#     db.init_app(app)
#     migrate = Migrate(app, db)

#     # Register blueprints
#     from .api import users, tasks 
#     app.register_blueprint(users.bp)
#     app.register_blueprint(tasks.bp)

#     return app

import os
from flask import Flask
from flask_migrate import Migrate

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True
    )

    if test_config is None:
        # Load the default config when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.update(test_config)

    if app.config.get('TESTING'):
        # Configure app for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Set up the database
    from .models import db
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register blueprints
    from .api import users, tasks 
    app.register_blueprint(users.bp)
    app.register_blueprint(tasks.bp)

    return app
