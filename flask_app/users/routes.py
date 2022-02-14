from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..models import User
from ..forms import LoginForm, RegistrationPersonalForm, RegistrationBusinessForm

users = Blueprint("users", __name__)


@users.route("/register/business", methods=["GET", "POST"])
def register_business():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for("users.register_personal"))

    form = RegistrationBusinessForm()

    if form.validate_on_submit():
        return render_template("register.html", form=form)

    return render_template("register.html", form=form, formTitle="注册企业账号")


@users.route("/register/personal", methods=["GET", "POST"])
def register_personal():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for("users.register_personal"))

    form = RegistrationPersonalForm()

    if form.validate_on_submit():
        return render_template("register.html", form=form)

    return render_template("register.html", form=form, formTitle="注册个人账号")


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
