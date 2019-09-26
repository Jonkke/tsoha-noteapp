from app import db
from app.models import Base

userNoteRead = db.Table("userNoteRead",
                        db.Column("user_id", db.Integer, db.ForeignKey("account.id"), primary_key=True),
                        db.Column("note_id", db.Integer, db.ForeignKey("note.id"), primary_key=True)
)

userNoteWrite = db.Table("userNoteWrite",
                        db.Column("user_id", db.Integer, db.ForeignKey("account.id"), primary_key=True),
                        db.Column("note_id", db.Integer, db.ForeignKey("note.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "account"

    username = db.Column(db.String(144), nullable=False)
    password_hash = db.Column(db.String(144), nullable=False)
    readableNotes = db.relationship("Note", secondary=userNoteRead, lazy="subquery",
        backref=db.backref("readUsers", lazy="dynamic"))
    writableNotes = db.relationship("Note", secondary=userNoteWrite, lazy="subquery",
        backref=db.backref("writeUsers", lazy="dynamic"))

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True