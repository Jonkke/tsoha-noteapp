from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

from app import app, db
from app.auth.models import User
from app.auth.forms import LoginForm, RegisterForm, PasswordChangeForm, InviteForm

bcrypt = Bcrypt(app)


@app.route("/auth/register", methods=["GET", "POST"])
def register_user():
    if request.method == "GET":
        return render_template("auth/registerform.html", form=RegisterForm())

    form = RegisterForm(request.form)

    # Existing user check & form validation
    user = User.query.filter_by(username=form.username.data).first()
    if (user):
        return render_template("auth/registerform.html", form=form, error="Username " + form.username.data + " is in use!")
    if not form.validate():
        return render_template("auth/registerform.html", form=form)

    pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    new_user = User(form.username.data, pw_hash)

    db.session().add(new_user)
    db.session().commit()

    return redirect(url_for("auth_login", regSuccess="1"))


@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        regSuccessMsg = ""
        if request.args.get("regSuccess"):
            regSuccessMsg = "Successfully registered a new user! You can now log in."
        return render_template("auth/loginform.html", form=LoginForm(), regSuccessMsg=regSuccessMsg)

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, form.password.data):
        return render_template("auth/loginform.html", form=form, error="No such username or password")

    login_user(user)
    return redirect(url_for("notes_index"))


@app.route("/auth/logout", methods=["GET"])
@login_required
def auth_logout():
    logout_user()
    return redirect(url_for("auth_login"))


@app.route("/auth/settings", methods=["GET"])
@login_required
def auth_settings():
    return render_accountsettings()


@app.route("/auth/pwupdate", methods=["POST"])
@login_required
def auth_pwupdate():
    form = PasswordChangeForm(request.form)
    if not bcrypt.check_password_hash(current_user.password_hash, form.oldpassword.data):
        return render_accountsettings(passwordMsg="Old password is wrong! Please try again.")

    pw_hash = bcrypt.generate_password_hash(
        form.newpassword.data).decode("utf-8")
    current_user.password_hash = pw_hash
    db.session().commit()

    return render_accountsettings(passwordMsg="Password has been changed.")


@app.route("/auth/invitecontact", methods=["POST"])
@login_required
def auth_invite():
    inviteForm = InviteForm(request.form)
    if not inviteForm.validate():
        return render_accountsettings(inviteForm=inviteForm)

    invitedUser = User.query.filter_by(
        five_letter_identifier=inviteForm.user_identifier.data.upper()).first()
    if invitedUser:
        if invitedUser.id == current_user.id:
            return render_accountsettings(inviteForm=inviteForm, invitedDoneMsg="Can't send invitation to yourself!")

        for contact in current_user.get_contact_list(include_non_confirmed=True):
            if (contact["id"] == invitedUser.id):
                return render_accountsettings(inviteForm=inviteForm,
                                              invitedDoneMsg="You already have a contact who has this invitation identifier! \
                                                             (This could be a pending contact that has not been accepted yet!)")

        query = "INSERT INTO user_contact (user_id, contact_id, inviter, confirmed) VALUES (:uid1, :uid2, :inv, '0')"
        db.session().execute(
            query, {'uid1': current_user.id, 'uid2': invitedUser.id, 'inv': current_user.id})
        db.session().execute(
            query, {'uid1': invitedUser.id, 'uid2': current_user.id, 'inv': current_user.id})
        db.session().commit()

    return render_accountsettings(invitedDoneMsg="Invitation sent. You must wait for the other user to accept your invitation.")


@app.route("/auth/acceptcontact/<contact_id>", methods=["POST"])
@login_required
def accept_contact(contact_id):
    query = "UPDATE user_contact SET confirmed='1' WHERE user_id=:uid1 AND contact_id=:uid2"
    db.session().execute(query, {'uid1': current_user.id, 'uid2': contact_id})
    db.session().execute(query, {'uid1': contact_id, 'uid2': current_user.id})
    db.session().commit()
    return redirect(url_for("auth_settings"))


@app.route("/auth/rejectcontact<contact_id>", methods=["POST"])
@login_required
def reject_contact(contact_id):
    query = "DELETE FROM user_contact WHERE user_id = :uid1 AND contact_id = :uid2"
    db.session().execute(query, {'uid1': current_user.id, 'uid2': contact_id})
    db.session().execute(query, {'uid1': contact_id, 'uid2': current_user.id})
    db.session().commit()
    return redirect(url_for("auth_settings"))

# helpers


def render_accountsettings(passwordChangeForm=None,
                           inviteForm=None,
                           invitedDoneMsg="",
                           passwordMsg=""):
    return render_template("auth/accountsettings.html",
                           contactlist=current_user.get_contact_list(),
                           pendingContactList=current_user.get_pending_contacts(),
                           pwchangeform=passwordChangeForm if passwordChangeForm else PasswordChangeForm(
                               passwordChangeForm),
                           passwordMsg=passwordMsg,
                           inviteForm=inviteForm if inviteForm else InviteForm(),
                           invitedDoneMsg=invitedDoneMsg)
