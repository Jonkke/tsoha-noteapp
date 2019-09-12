from app import app, db
from flask import redirect, url_for, render_template, request
from app.notes.models import Note

@app.route("/notes", methods=["GET"])
def notes_index():
    notes = Note.query.all()
    return render_template("notes/notelist.html", notes=notes)

@app.route("/notes/new")
def notes_form():
    return render_template("notes/newnote.html")

@app.route("/notes/", methods=["POST"])
def notes_create():
    note = Note(request.form.get("title"), request.form.get("content"), 0, 1 if request.form.get("is_shared") == "on" else 0, 0)
    db.session().add(note)
    db.session().commit()

    return redirect(url_for("notes_index"))

@app.route("/notes/<note_id>", methods=["GET"])
def notes_edit(note_id):
    note = Note.query.get(note_id)
    #print("Note is:\n\n" + note + "\n\n")
    return render_template("notes/newnote.html", note=note)

@app.route("/notes/edit/<note_id>/", methods=["POST"])
def notes_update(note_id):
    note = Note.query.get(note_id)
    note.title = request.form.get("title")
    note.content = request.form.get("content")
    note.is_shared = 1 if request.form.get("is_shared") == "on" else 0
    db.session().commit()

    return render_template("notes/notelist.html", notes=Note.query.all())

@app.route("/notes/delete/<note_id>/", methods=["POST"])
def notes_delete(note_id):
    note = Note.query.get(note_id)
    db.session().delete(note)
    db.session().commit()

    return render_template("notes/notelist.html", notes=Note.query.all())