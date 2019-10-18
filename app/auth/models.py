import random
import string
from app import db
from app.models import Base
from sqlalchemy.ext.declarative import declarative_base

table_base = declarative_base()

user_note_read = db.Table("user_note_read",
                          db.Column("user_id", db.Integer, db.ForeignKey(
                              "account.id"), primary_key=True),
                          db.Column("note_id", db.Integer, db.ForeignKey(
                              "note.id"), primary_key=True)
                          )

user_note_write = db.Table("user_note_write",
                           db.Column("user_id", db.Integer, db.ForeignKey(
                               "account.id"), primary_key=True),
                           db.Column("note_id", db.Integer, db.ForeignKey(
                               "note.id"), primary_key=True)
                           )

user_contact = db.Table("user_contact", db.Model.metadata,
                        db.Column("user_id", db.Integer, db.ForeignKey(
                            "account.id"), primary_key=True),
                        db.Column("contact_id", db.Integer, db.ForeignKey(
                            "account.id"), primary_key=True),
                        db.Column("inviter", db.Integer, db.ForeignKey(
                            "account.id"), nullable=False),
                        db.Column("confirmed", db.Boolean, default=False),
                        db.Column("date_contacted", db.DateTime,
                                  default=db.func.current_timestamp())
                        )


class User(Base):
    __tablename__ = "account"

    username = db.Column(db.String(144), nullable=False)
    password_hash = db.Column(db.String(144), nullable=False)
    five_letter_identifier = db.Column(db.String(5), nullable=False)
    readableNotes = db.relationship("Note", secondary=user_note_read, lazy="dynamic",
                                    backref=db.backref("readUsers", lazy="dynamic"))
    writableNotes = db.relationship("Note", secondary=user_note_write, lazy="dynamic",
                                    backref=db.backref("writeUsers", lazy="dynamic"))
    contacts = db.relationship("User",
                               secondary=user_contact,
                               primaryjoin="User.id == user_contact.c.user_id",
                               secondaryjoin="User.id == user_contact.c.contact_id",
                               backref=db.backref("contactees", lazy="dynamic")
                               )

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

        char_pool = string.ascii_uppercase.join(
            string.digits).join(string.digits)
        five_letter_identifier = "".join(
            random.choice(char_pool) for i in range(5))
        # loop while identifier already in use
        while len(db.session().execute("SELECT * FROM account WHERE five_letter_identifier = :fli", {"fli": five_letter_identifier}).fetchall()):
            five_letter_identifier = "".join(
                random.choice(char_pool) for i in range(5))
        self.five_letter_identifier = five_letter_identifier

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_notes_count(self, count_filter="all"):
        count = 0
        if count_filter == "owned_only":
            query = "SELECT COUNT (*) FROM note n WHERE n.creator_id = :uid"
            count = db.session().execute(query, {'uid': self.id}).scalar()
        elif count_filter == "not_owned_readable":
            query = "SELECT COUNT (*) FROM \
                    (note n INNER JOIN user_note_read unr ON n.id = unr.note_id AND n.creator_id != unr.user_id) \
                     WHERE user_id = :uid"
            count = db.session().execute(query, {'uid': self.id}).scalar()
        elif count_filter == "not_owned_writable":
            query = "SELECT COUNT (*) FROM \
                     (note n INNER JOIN user_note_write unw ON n.id = unw.note_id AND n.creator_id != unw.user_id) \
                     WHERE user_id = :uid"
            count = db.session().execute(query, {'uid': self.id}).scalar()
        elif count_filter == "all":
            query = "SELECT COUNT (*) FROM \
                    (note n INNER JOIN user_note_read unr ON n.id = unr.note_id) \
                    WHERE user_id = :uid"
            count = db.session().execute(query, {'uid': self.id}).scalar()
        else:
            count = 0
        return count

    def get_contact_list(self, include_non_confirmed=False):
        query = ""
        if not include_non_confirmed:
            query = "SELECT * FROM \
                    (account a INNER JOIN user_contact uc ON uc.user_id = a.id AND uc.contact_id != a.id AND uc.confirmed = '1') ac \
                     WHERE ac.id != :uid AND ac.contact_id = :uid"
        else:
            query = "SELECT * FROM \
                    (account a INNER JOIN user_contact uc ON uc.user_id = a.id AND uc.contact_id != a.id) ac \
                     WHERE ac.id != :uid AND ac.contact_id = :uid"
        rs = db.session().execute(query, {'uid': self.id})
        contacts = []
        for r in rs:
            contacts.append(dict(r.items()))
        return list(
            map(lambda contact: {"id": contact["id"],
                                 "username": contact["username"]}, contacts))

    def get_pending_contacts(self):
        query = "SELECT * FROM \
                (account a INNER JOIN user_contact uc ON uc.user_id = a.id AND uc.contact_id != a.id AND uc.confirmed = '0') ac \
                WHERE ac.id != :uid AND ac.contact_id = :uid AND ac.inviter != :uid"
        rs = db.session().execute(query, {'uid': self.id})
        pendingContacts = []
        for r in rs:
            pendingContacts.append(dict(r.items()))
        return list(
            map(lambda pendingContact: {
                "id": pendingContact["id"],
                "username": pendingContact["username"]}, pendingContacts))
