from flask import render_template
from app import app
from flask_moment import Moment
moment = Moment(app)

@app.route("/")
def index():
    return render_template("index.html")
