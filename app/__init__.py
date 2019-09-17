from flask import Flask
app = Flask(__name__)

import os
from flask_sqlalchemy import SQLAlchemy

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from app import views

#import notes
from app.notes import models
from app.notes import views

#import views
from app.auth import models
from app.auth import views

#login
from app.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Log in to use this functionality"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

try:
    db.create_all()
except:
    pass