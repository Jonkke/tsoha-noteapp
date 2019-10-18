from flask import render_template, redirect, url_for
from app import app
from flask_moment import Moment
moment = Moment(app)

@app.route("/")
def index():
    return redirect(url_for('notes_index'))