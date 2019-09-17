from app import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    title = db.Column(db.String())
    content = db.Column(db.String(), default="")
    is_shared = db.Column(db.Boolean)
    is_archived = db.Column(db.Boolean)

    def __init__(self, title, content, creator_id, is_shared, is_archived):
        self.title = title
        self.content = content
        self.creator_id = creator_id
        self.is_archived = is_archived
        self.is_shared = is_shared

    def __str__(self):
        return "Title: " + self.title + "\nContent: " + self.content
        