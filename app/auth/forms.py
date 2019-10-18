from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import EqualTo

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=2, max=32)])
    password = PasswordField("Password", validators=[validators.Length(min=4, max=128), validators.EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField("Repeat password")

    class Meta:
        csrf = False

class PasswordChangeForm(FlaskForm):
    oldpassword = PasswordField("Old password")
    newpassword = PasswordField("Password", [validators.Length(min=4), validators.Length(max=128)])

    class Meta:
        csrf = False

class InviteForm(FlaskForm):
    user_identifier = StringField("Identifier", [validators.Length(min=5, max=5)])

    class Meta:
        csrf = False