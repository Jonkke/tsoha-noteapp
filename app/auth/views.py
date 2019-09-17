from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from flask_bcrypt import Bcrypt

from app import app
from app.auth.models import User
from app.auth.forms import LoginForm

bcrypt = Bcrypt(app)

@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())
    
    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data).first()
    if not user or not bcrypt.check_password_hash(user.password, form.password.data):
        return render_template("auth/loginform.html", form=form, error="No such username or password")

    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/logout", methods=["GET"])
def auth_logout():
    logout_user()
    return redirect(url_for("index"))
