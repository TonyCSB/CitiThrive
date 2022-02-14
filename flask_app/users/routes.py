from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..models import User
from ..forms import LoginForm

users = Blueprint("users", __name__)


@users.route("/register/business", methods=["GET", "POST"])
def register_business():
    return render_template("plaintext.html", content="Business User Registration")

@users.route("/register/personal", methods=["GET", "POST"])
def register_personal():
    return render_template("plaintext.html", content="Consumer User Registration")


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("account"))

    form = LoginForm()

    if form.validate_on_submit():
        return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@users.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage.index"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    return render_template("plaintext.html", content="User Account Detail")
