from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=2), validators.Length(max=32)])
    password = PasswordField("Password", [validators.Length(min=4), validators.Length(max=128)])

    class Meta:
        csrf = False
