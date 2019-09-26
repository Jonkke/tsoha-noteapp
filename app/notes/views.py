from app import app, db
from flask import redirect, url_for, render_template, request
from flask_login import login_required, current_user

from app.notes.models import Note
from app.notes.forms import NoteForm

@app.route("/notes", methods=["GET"])
@login_required
def notes_index():
    notes = Note.query.all()
    return render_template("notes/notelist.html", notes=notes)

@app.route("/notes/new")
@login_required
def notes_form():
    return render_template("notes/newnote.html", form=NoteForm())

@app.route("/notes/", methods=["POST"])
@login_required
def notes_create():
    form = NoteForm(request.form)

    if not form.validate():
        return render_template("notes/newnote.html", form=form)

    note = Note(form.title.data, form.content.data, current_user.id, form.is_shared.data, 0)
    db.session().add(note)
    db.session().commit()

    return redirect(url_for("notes_index"))

@app.route("/notes/<note_id>", methods=["GET"])
@login_required
def notes_edit(note_id):
    form = NoteForm()
    note = Note.query.get(note_id)
    form.title.data = note.title
    form.content.data = note.content
    form.is_shared.data = note.is_shared
    return render_template("notes/newnote.html", form=form, note_id=note.id)

@app.route("/notes/edit/<note_id>/", methods=["POST"])
@login_required
def notes_update(note_id):
    form = NoteForm(request.form)

    if not form.validate():
        return render_template("notes/newnote.html", form=form, note_id=note_id)

    note = Note.query.get(note_id)
    note.title = request.form.get("title")
    note.content = request.form.get("content")
    note.is_shared = 1 if request.form.get("is_shared") == "on" else 0
    note.last_editor_id = current_user.id
    db.session().commit()

    return render_template("notes/notelist.html", notes=Note.query.all())

@app.route("/notes/delete/<note_id>/", methods=["POST"])
@login_required
def notes_delete(note_id):
    note = Note.query.get(note_id)
    db.session().delete(note)
    db.session().commit()

    return render_template("notes/notelist.html", notes=Note.query.all())
