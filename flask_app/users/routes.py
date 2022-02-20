from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..models import User, ConsumerUser, BusinessUser
from ..forms import LoginForm, RegistrationConsumerForm, RegistrationBusinessForm

users = Blueprint("users", __name__)


@users.route("/register/business", methods=["GET", "POST"])
def register_business():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for("users.register_consumer"))

    form = RegistrationBusinessForm()

    if form.validate_on_submit():
        # TODO: Password validation

        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        detail = BusinessUser(idCode=form.id.data, companyName=form.companyName.data, stockCode=form.stockCode.data)
        detail.save()

        user = User(username=form.username.data, email=form.email.data, password=hashed, type="business", detail=detail)
        user.save()

        return redirect(url_for("users.login"))

    return render_template("register.html", form=form, formTitle="注册企业账号")


@users.route("/register/consumer", methods=["GET", "POST"])
def register_consumer():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for("users.register_consumer"))

    form = RegistrationConsumerForm()

    if form.validate_on_submit():
        # TODO: Password validation

        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        detail = ConsumerUser(idCode=form.id.data)
        detail.save()

        user = User(username=form.username.data, email=form.email.data, password=hashed, type="consumer", detail=detail)
        user.save()

        return redirect(url_for("users.login"))

    return render_template("register.html", form=form, formTitle="注册个人账号")


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("account"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user is None:
            flash("Username does not exist!")
        elif not bcrypt.check_password_hash(user.password, form.password.data):
            flash("Username/Password incorrect!")
        elif form.accountType.data != user.type:
            flash("请选择正确的账号类别")
        else:
            login_user(user)

            if request.args.get("next") is not None:
                return redirect(request.args.get("next"))
            else:
                return redirect(url_for("homepage.index"))

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
