from app import db
from app.models import Base
from sqlalchemy.orm import relationship

# noteTag = db.Table("noteTag",
#                     db.Column("note_id", db.Integer, db.ForeignKey("note.id"), primary_key=True),
#                     db.Column("tag_id", db.Integer, db.ForeignKey("tag.id", primary_key=True))                    
# )

class Note(Base):
    creator_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    last_editor_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    title = db.Column(db.String())
    content = db.Column(db.String(), default="")
    is_shared = db.Column(db.Boolean)
    is_archived = db.Column(db.Boolean)
    creator = relationship("User", foreign_keys=[creator_id])
    last_editor = relationship("User", foreign_keys=[last_editor_id])

    def __init__(self, title, content, creator_id, is_shared, is_archived):
        self.title = title
        self.content = content
        self.creator_id = creator_id
        self.last_editor_id = creator_id
        self.is_archived = is_archived
        self.is_shared = is_shared

    def __str__(self):
        return "Title: " + self.title + "\nContent: " + self.content
        
    
# class Tag(Base):
#     name = db.Column(db.String(32), nullable=False)