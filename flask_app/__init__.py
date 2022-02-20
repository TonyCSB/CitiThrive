from flask import Flask, render_template, redirect, url_for, request
from flask_mongoengine import MongoEngine
from flask_talisman import Talisman
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = MongoEngine()
bcrypt = Bcrypt()
login_manager = LoginManager()

from .homepage.routes import homepage
from .users.routes import users

CSP = {
    'default-src': ['\'self\''],
    'img-src': ['\'self\'', 'data:', 'www.googletagmanager.com'],
    'script-src': ['\'self\'', 'www.googletagmanager.com']
}


def page_not_found(e):
    return render_template("404.html"), 404


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    Talisman(app, content_security_policy=CSP, force_https=False)

    app.register_error_handler(404, page_not_found)

    app.register_blueprint(homepage)
    app.register_blueprint(users, url_prefix="/user")

    login_manager.login_view = "users.login"

    return app


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for("users.login") + "?next=" + request.path)
