from flask import Flask
from flask_mongoengine import MongoEngine
from flask_talisman import Talisman

from .homepage.routes import homepage

db = MongoEngine()

CSP = {
    'default-src': ['\'self\'']
}


def page_not_found(e):
    return "Page Not Found", 404


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)

    db.init_app(app)
    Talisman(app, content_security_policy=CSP, force_https=False)

    app.register_error_handler(404, page_not_found)

    app.register_blueprint(homepage)

    return app
