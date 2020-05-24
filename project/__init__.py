import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


load_dotenv()

session = Session()
db = SQLAlchemy()
bcrypt = Bcrypt()

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Error handler


def page_not_found(e):
    return render_template('404.html'), 404


def create_app(script_info=None):

    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    session.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)

    # Error handlers
    app.register_error_handler(404, page_not_found)

    # set up blueprints
    from project.books.routes import books_blueprint
    from project.auth.routes import auth_blueprint
    from project.reviews.routes import reviews_blueprint
    from project.api.routes import api_blueprint

    app.register_blueprint(books_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(reviews_blueprint)
    app.register_blueprint(api_blueprint)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
