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
            regSuccessMsg = "Successfully registered new user! You can now log in."
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
        return render_accountsettings(passwordMsg="Wrong password.")

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
        five_letter_identifier=inviteForm.user_identifier.data).first()
    if invitedUser:
        if invitedUser.id == current_user.id:
            return render_accountsettings(inviteForm=inviteForm)

        for contact in get_contact_list(includeNonConfirmed=True):
            if (contact["id"] == invitedUser.id):
                return render_accountsettings(inviteForm=inviteForm)

        query = "INSERT INTO userContact (user_id, contact_id, inviter, confirmed) VALUES (:uid1, :uid2, :inv, 0)"
        # current_user.contacts.append(invitedUser)
        # invitedUser.contacts.append(current_user)
        # db.session().commit()
        db.session.execute(
            query, {'uid1': current_user.id, 'uid2': invitedUser.id, 'inv': current_user.id})
        db.session.execute(
            query, {'uid1': invitedUser.id, 'uid2': current_user.id, 'inv': current_user.id})
        db.session.commit()

    return render_accountsettings(invitedDoneMsg="Invitation sent, awaiting confirmation from the other user.")


@app.route("/auth/acceptcontact/<contact_id>", methods=["POST"])
@login_required
def accept_contact(contact_id):
    query = "UPDATE userContact SET confirmed=1 WHERE user_id=:uid1 AND contact_id=:uid2"
    db.session.execute(query, {'uid1': current_user.id, 'uid2': contact_id})
    db.session.execute(query, {'uid1': contact_id, 'uid2': current_user.id})
    db.session.commit()
    return redirect(url_for("auth_settings"))


@app.route("/auth/rejectcontact<contact_id>", methods=["POST"])
@login_required
def reject_contact(contact_id):
    return redirect(url_for("auth_settings"))

# helpers


def get_user_info():
    return {
        "username": current_user.username,
        "five_letter_identifier": current_user.five_letter_identifier,
        "numcontacts": len(current_user.contacts)
    }


def get_contact_list(includeNonConfirmed=False):
    query = ""
    if not includeNonConfirmed:
        query = "SELECT * FROM (account a INNER JOIN userContact uc ON uc.user_id = a.id AND uc.contact_id != a.id AND uc.confirmed = 1) ac WHERE ac.id != :uid AND ac.contact_id = :uid"
    else:
        query = "SELECT * FROM (account a INNER JOIN userContact uc ON uc.user_id = a.id AND uc.contact_id != a.id) ac WHERE ac.id != :uid AND ac.contact_id = :uid"
    rs = db.session.execute(query, {'uid': current_user.id})
    contacts = []
    for r in rs:
        contacts.append(dict(r.items()))
    return list(
        map(lambda contact: {"id": contact["id"],
                             "username": contact["username"]}, contacts))


def get_pending_contacts():
    query = "SELECT * FROM (account a INNER JOIN userContact uc ON uc.user_id = a.id AND uc.contact_id != a.id AND uc.confirmed = 0) ac WHERE ac.id != :uid AND ac.contact_id = :uid AND ac.inviter != :uid"
    rs = db.session.execute(query, {'uid': current_user.id})
    pendingContacts = []
    for r in rs:
        pendingContacts.append(dict(r.items()))
    return list(
        map(lambda pendingContact: {
            "id": pendingContact["id"],
            "username": pendingContact["username"]}, pendingContacts))


def render_accountsettings(get_user_info=get_user_info,
                           get_contact_list=get_contact_list,
                           get_pending_contacts=get_pending_contacts,
                           passwordChangeForm=None,
                           inviteForm=None,
                           invitedDoneMsg="",
                           passwordMsg=""):
    return render_template("auth/accountsettings.html", userinfo=get_user_info(),
                           contactlist=get_contact_list(),
                           pendingContactList=get_pending_contacts(),
                           pwchangeform=passwordChangeForm if passwordChangeForm else PasswordChangeForm(passwordChangeForm),
                           passwordMsg=passwordMsg,
                           inviteForm=inviteForm if inviteForm else InviteForm(),
                           invitedDoneMsg=invitedDoneMsg)
