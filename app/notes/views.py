from app import app, db
from flask import redirect, url_for, render_template, request
from flask_login import login_required, current_user

from app.auth.models import User
from app.notes.models import Note, Tag
from app.notes.forms import NoteForm, NoteSearchForm


@app.route("/notes", methods=["GET"])
@login_required
def notes_index():
    notes = current_user.readableNotes
    noNotesMsg = "No notes to display." if not notes else ""
    return render_template("notes/notelist.html", notes=notes, form=NoteSearchForm(), noNotesMsg=noNotesMsg, uid=current_user.id, writableNotes=current_user.writableNotes)


@app.route("/notes/search", methods=["POST"])
@login_required
def notes_search():
    form = NoteSearchForm(request.form)
    searchedTags = list(form.search_str.data.split())
    if not searchedTags:
        return redirect(url_for("notes_index"))
    notes = current_user.readableNotes
    filteredNotes = []
    for note in notes:
        for tag in note.tags:
            if [stag for stag in searchedTags if stag in tag.name]:
                filteredNotes.append(note)
                break
            # if searchedTags.count(tag.name):
            #     filteredNotes.append(note)
            #     break

    noNotesMsg = "Search did not match any notes." if not filteredNotes else ""

    return render_template("notes/notelist.html", notes=filteredNotes, form=NoteSearchForm(), activeFilterTags=searchedTags, noNotesMsg=noNotesMsg, uid=current_user.id, writableNotes=current_user.writableNotes)


@app.route("/notes/new")
@login_required
def notes_form():
    return render_newnote()


@app.route("/notes/", methods=["POST"])
@login_required
def notes_create():
    form = NoteForm(request.form)
    if not form.validate():
        return render_newnote(form=form)

    note = Note(form.title.data, form.content.data,
                current_user.id)

    # parse tags & associate with this note
    formTagNames = list(dict.fromkeys(form.tags.data.split()))
    oldTagNames = list(map(lambda tag: tag.name, Tag.query.all()))
    newTags = []
    for tagName in formTagNames:
        if not oldTagNames.count(tagName):
            newTags.append(Tag(tagName))

    if newTags:
        db.session().add_all(newTags)

    associatedTags = list(
        filter(lambda tag: formTagNames.count(tag.name), Tag.query.all()))
    note.tags = associatedTags
    db.session().add(note)

    # add read and write right to creator of this note
    current_user.readableNotes.append(note)
    current_user.writableNotes.append(note)
    # and to other(s) if shared
    # write right
    if form.writeShareWith.data != 0:
        user = User.query.get(form.writeShareWith.data)
        if user:
            user.writableNotes.append(note)
            if not note in user.readableNotes:
                user.readableNotes.append(note)

    # read right
    if form.readShareWith.data != 0 and form.readShareWith.data != form.writeShareWith.data:
        user = User.query.get(form.readShareWith.data)
        if user:
            user.readableNotes.append(note)

    db.session().add(current_user)

    db.session().commit()

    return redirect(url_for("notes_index"))


@app.route("/notes/<note_id>", methods=["GET"])
@login_required
def notes_edit(note_id):
    form = NoteForm()
    note = Note.query.get(note_id)

    if not note or note.writeUsers.filter_by(id=current_user.id).first() is None:
        return redirect(url_for("notes_index", error="You do not have rights to edit this note!"))

    form.title.data = note.title
    form.content.data = note.content
    form.tags.data = " ".join(map(str, note.tags.all()))
    allowsharing = True if current_user.id == note.creator_id else False
    read_users = filter(lambda user: user.id !=
                        current_user.id, note.readUsers)
    write_users = filter(lambda user: user.id !=
                         current_user.id, note.writeUsers)
    return render_newnote(form=form, note_id=note_id, allowsharing=allowsharing, read_users=read_users, write_users=write_users)


@app.route("/notes/edit/removerights/", methods=["GET"])
@login_required
def note_remove_rights():
    user_id = request.args.get("user_id")
    note_id = request.args.get("note_id")
    write_only = request.args.get("write_only")
    user = User.query.filter_by(id=user_id).first()
    note = Note.query.filter_by(id=note_id).first()
    if not user or not note or current_user.id != note.creator_id:
        return redirect(url_for("notes_index"))
    if write_only:
        user.writableNotes.remove(note)
    else:
        user.readableNotes.remove(note)
        if user in note.writeUsers:
            user.writableNotes.remove(note)
    db.session().commit()
    return redirect(url_for("notes_edit", note_id=note_id))


@app.route("/notes/edit/<note_id>/", methods=["POST"])
@login_required
def notes_update(note_id):
    form = NoteForm(request.form)

    if not form.validate():
        return render_newnote(form=form, note_id=note_id)

    note = Note.query.get(note_id)

    if note.writeUsers.filter_by(id=current_user.id).first() is None:
        return redirect(url_for("notes_index"))

    note.title = request.form.get("title")
    note.content = request.form.get("content")
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

    associatedTags = list(
        filter(lambda tag: formTagNames.count(tag.name), Tag.query.all()))
    note.tags = associatedTags

    # handle further sharing of this note
    # write right
    if note.creator_id == current_user.id and form.writeShareWith.data != 0:
        user = User.query.get(form.writeShareWith.data)
        if user and not note in user.writableNotes:
            user.writableNotes.append(note)
            if not note in user.readableNotes:
                user.readableNotes.append(note)

    # read right
    if note.creator_id == current_user.id and form.readShareWith.data != 0 and form.readShareWith.data != form.writeShareWith.data:
        user = User.query.get(form.readShareWith.data)
        if user and not note in user.readableNotes:
            user.readableNotes.append(note)

    db.session().commit()

    notes = current_user.readableNotes
    return render_template("notes/notelist.html", notes=notes, form=NoteSearchForm(), uid=current_user.id, writableNotes=current_user.writableNotes)


@app.route("/notes/delete/<note_id>/", methods=["POST"])
@login_required
def notes_delete(note_id):
    note = Note.query.get(note_id)

    if note.writeUsers.filter_by(id=current_user.id).first() is None:
        return redirect(url_for("notes_index"))

    db.session().delete(note)
    db.session().commit()

    notes = current_user.readableNotes

    return render_template("notes/notelist.html", notes=notes, form=NoteSearchForm(), uid=current_user.id, writableNotes=current_user.writableNotes)


# helpers

def render_newnote(form=None,
                   note_id=None,
                   allowsharing=False,
                   read_users=[],
                   write_users=[]):
    contacts = [{"id": 0, "username": "None"}] + \
        current_user.get_contact_list()
    form = form if form else NoteForm()
    form.readShareWith.choices = [(c["id"], c["username"]) for c in contacts]
    form.writeShareWith.choices = [(c["id"], c["username"]) for c in contacts]
    return render_template("notes/newnote.html",
                           form=form,
                           note_id=note_id,
                           allowsharing=allowsharing,
                           read_users=read_users,
                           write_users=write_users)
