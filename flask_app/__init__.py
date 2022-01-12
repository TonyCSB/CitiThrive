from flask import Flask
from flask_mongoengine import MongoEngine

db = MongoEngine()

from .test.routes import test


def page_not_found(e):
    return "Page Not Found", 404


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)

    db.init_app(app)

    app.register_error_handler(404, page_not_found)

    app.register_blueprint(test)

    return app
