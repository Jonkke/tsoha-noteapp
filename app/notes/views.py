from app import app, db
from flask import redirect, url_for, render_template, request
from flask_login import login_required, current_user

from app.notes.models import Note, Tag
from app.notes.forms import NoteForm, NoteSearchForm

@app.route("/notes", methods=["GET"])
@login_required
def notes_index():
    #notes = Note.query.all()
    notes = current_user.readableNotes
    return render_template("notes/notelist.html", notes=notes, form=NoteSearchForm())

@app.route("/notes/search", methods=["POST"])
@login_required
def notes_search():
    form = NoteSearchForm(request.form)
    searchedTags = form.search_str.data.split()
    notes = current_user.readableNotes
    filteredNotes = []
    for note in notes:
        for tag in note.tags:
            if searchedTags.count(tag.name):
                filteredNotes.append(note)
                break

    return render_template("notes/notelist.html", notes=filteredNotes, form=NoteSearchForm())

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

    # parse tags & associate with this note
    formTagNames = list(dict.fromkeys(form.tags.data.split()))
    oldTagNames = list(map(lambda tag: tag.name, Tag.query.all()))
    newTags = []
    for tagName in formTagNames:
        if not oldTagNames.count(tagName):
            newTags.append(Tag(tagName))

    if newTags:
        db.session().add_all(newTags)

    associatedTags = list(filter(lambda tag: formTagNames.count(tag.name), Tag.query.all()))
    note.tags = associatedTags
    db.session().add(note)

    # add read and write right to creator of this note
    current_user.readableNotes.append(note)
    current_user.writableNotes.append(note)
    db.session().add(current_user)

    db.session().commit()

    return redirect(url_for("notes_index"))

@app.route("/notes/<note_id>", methods=["GET"])
@login_required
def notes_edit(note_id):
    form = NoteForm()
    note = Note.query.get(note_id)

    if note.writeUsers.filter_by(id=current_user.id).first() is None:
        return redirect(url_for("notes_index", error="You do not have rights to edit this note!"))

    form.title.data = note.title
    form.content.data = note.content
    form.is_shared.data = note.is_shared
    form.tags.data = " ".join(map(str, note.tags.all()))
    return render_template("notes/newnote.html", form=form, note_id=note.id)

@app.route("/notes/edit/<note_id>/", methods=["POST"])
@login_required
def notes_update(note_id):
    form = NoteForm(request.form)

    if not form.validate():
        return render_template("notes/newnote.html", form=form, note_id=note_id)

    note = Note.query.get(note_id)

    if note.writeUsers.filter_by(id=current_user.id).first() is None:
        return redirect(url_for("notes_index"))

    note.title = request.form.get("title")
    note.content = request.form.get("content")
    note.is_shared = 1 if request.form.get("is_shared") == "on" else 0
    note.last_editor_id = current_user.id

    # update tags
    formTagNames = list(dict.fromkeys(form.tags.data.split()))
    oldTagNames = list(map(lambda tag: tag.name, Tag.query.all()))
    newTags = []
    for tagName in formTagNames:
        if not oldTagNames.count(tagName):
            newTags.append(Tag(tagName))

    if newTags:
        db.session().add_all(newTags)

    associatedTags = list(filter(lambda tag: formTagNames.count(tag.name), Tag.query.all()))
    note.tags = associatedTags

    db.session().commit()

    notes = current_user.readableNotes
    return render_template("notes/notelist.html", notes=notes)

@app.route("/notes/delete/<note_id>/", methods=["POST"])
@login_required
def notes_delete(note_id):
    note = Note.query.get(note_id)

    if note.writeUsers.filter_by(id=current_user.id).first() is None:
        return redirect(url_for("notes_index"))

    db.session().delete(note)
    db.session().commit()

    notes = current_user.readableNotes

    return render_template("notes/notelist.html", notes=notes)
