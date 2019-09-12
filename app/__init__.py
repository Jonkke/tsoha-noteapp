from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from app import views

from app.notes import models
from app.notes import views

db.create_all()