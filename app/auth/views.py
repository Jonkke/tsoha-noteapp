from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from flask_bcrypt import Bcrypt

from app import app, db
from app.auth.models import User
from app.auth.forms import LoginForm
from app.auth.forms import RegisterForm

bcrypt = Bcrypt(app)

@app.route("/auth/register", methods=["GET", "POST"])
def register_user():
    if request.method == "GET":
        return render_template("auth/registerform.html", form=RegisterForm())

    form = RegisterForm(request.form)

    # Existing user check
    user = User.query.filter_by(username=form.username.data).first()
    print("user is: \n\n\n")
    print(user)
    if (user):
        return render_template("auth/registerform.html", form=form, error="Username " + form.username.data + " is in use!")

    pw_hash = bcrypt.generate_password_hash(form.password.data)
    new_user = User(form.username.data, pw_hash)

    db.session().add(new_user)
    db.session().commit()

    return redirect(url_for("index"))

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
