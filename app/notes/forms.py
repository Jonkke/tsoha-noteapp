from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, validators

class NoteForm(FlaskForm):
    title = StringField("Title", [validators.Length(min=2)])
    content = TextAreaField("Content")
    tags = StringField("Tags")
    is_shared = BooleanField("Shared")

    class Meta:
        csrf = False

class NoteSearchForm(FlaskForm):
    search_str = StringField("Search by tag(s):", [validators.Length(min=1)])

    class Meta:
        csrf = False