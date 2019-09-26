from app import db
from app.models import Base

class User(Base):
    __tablename__ = "account"

    username = db.Column(db.String(144), nullable=False)
    password_hash = db.Column(db.String(144), nullable=False)

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