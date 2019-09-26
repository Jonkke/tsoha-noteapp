from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, validators

class NoteForm(FlaskForm):
    title = StringField("Title", [validators.Length(min=2)])
    content = TextAreaField("Content")
    tags = StringField("Tags")
    is_shared = BooleanField("Shared")

    class Meta:
        csrf = False
