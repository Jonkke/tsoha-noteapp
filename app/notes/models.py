from app import db
from app.models import Base
from sqlalchemy.orm import relationship

note_tag = db.Table("note_tag",
                    db.Column("note_id", db.Integer, db.ForeignKey(
                        "note.id"), primary_key=True),
                    db.Column("tag_id", db.Integer, db.ForeignKey(
                        "tag.id"), primary_key=True)
                    )


class Note(Base):
    creator_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=False)
    last_editor_id = db.Column(
        db.Integer, db.ForeignKey('account.id'), nullable=False)
    title = db.Column(db.String())
    content = db.Column(db.String(), default="")
    creator = relationship("User", foreign_keys=[creator_id])
    last_editor = relationship("User", foreign_keys=[last_editor_id])
    tags = db.relationship("Tag", secondary=note_tag, lazy="dynamic",
                           backref=db.backref("notes", lazy="dynamic"))

    def __init__(self, title, content, creator_id):
        self.title = title
        self.content = content
        self.creator_id = creator_id
        self.last_editor_id = creator_id

    def __str__(self):
        return "Title: " + self.title + "\nContent: " + self.content


# Decided to keep Tag class here alongside Note, as it does not really contain much in terms of functionality
class Tag(Base):
    name = db.Column(db.String(32), nullable=False)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
