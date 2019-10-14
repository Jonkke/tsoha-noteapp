from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, validators

#overriden SelectField with disabled prevalidation
class NoValidationSelectField(SelectField):
    def pre_validate(self, form):
        """disabled"""

class NoteForm(FlaskForm):
    title = StringField("Title", [validators.Length(min=2)])
    content = TextAreaField("Content")
    tags = StringField("Tags")
    readShareWith = NoValidationSelectField("Add read rights", choices=[])
    writeShareWith = NoValidationSelectField("Add write rights", choices=[])

    class Meta:
        csrf = False

class NoteSearchForm(FlaskForm):
    search_str = StringField("Search by tag(s):", [validators.Length(min=1)])

    class Meta:
        csrf = False
