from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo
)


class LoginForm(FlaskForm):
    accountType = RadioField("Account Type", validators=[InputRequired()], choices=[(0, "企业账号"), (1, "个人账号")], default=0)
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")
