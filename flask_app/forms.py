from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError
)
from id_validator import validator


class LoginForm(FlaskForm):
    accountType = RadioField("Account Type", validators=[InputRequired()], choices=[("business", "企业账号"), ("consumer", "个人账号")], default="business")
    username = StringField("用户名", validators=[InputRequired()])
    password = PasswordField("密码", validators=[InputRequired()])
    submit = SubmitField("登陆")


class RegistrationBusinessForm(FlaskForm):
    username = StringField("用户名", validators=[InputRequired()], render_kw={'placeholder': 'username'})
    email = StringField("电子邮箱", validators=[InputRequired(), Email()], render_kw={'placeholder': 'email'})
    companyName = StringField("公司名称", validators=[InputRequired()], render_kw={'placeholder': 'XX公司'})
    stockCode = StringField("股票代码", render_kw={'placeholder': 'AAPL'})

    password = PasswordField("密码", validators=[InputRequired(), Length(min=8)], render_kw={'placeholder': 'password'})
    confirm_pwd = PasswordField("请确认密码", validators=[InputRequired(), EqualTo("password")], render_kw={'placeholder': 'password'})

    submit = SubmitField("注册", render_kw={'class': 'btn btn-primary btn-login text-uppercase fw-bold'})


class RegistrationConsumerForm(FlaskForm):
    username = StringField("用户名", validators=[InputRequired()], render_kw={'placeholder': 'username'})
    email = StringField("电子邮箱", validators=[InputRequired(), Email()], render_kw={'placeholder': 'email'})
    id = StringField("身份证号码", validators=[InputRequired(), Length(min=15, max=18)], render_kw={'placeholder': '310110194910011008'})

    password = PasswordField("密码", validators=[InputRequired(), Length(min=8)], render_kw={'placeholder': 'password'})
    confirm_pwd = PasswordField("请确认密码", validators=[InputRequired(), EqualTo("password")], render_kw={'placeholder': 'password'})

    submit = SubmitField("注册", render_kw={'class': 'btn btn-primary btn-login text-uppercase fw-bold'})

    def validate_id(form, field):
        if not validator.is_valid(field.data):
            raise ValidationError("身份证号码校验失败")
