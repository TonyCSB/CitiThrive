from flask import Flask

from .test.routes import test


def page_not_found(e):
    return "Page Not Found", 404


def create_app():
    app = Flask(__name__)
    app.register_error_handler(404, page_not_found)

    app.register_blueprint(test)

    return app
