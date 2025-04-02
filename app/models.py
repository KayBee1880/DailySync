from database import db
from flask_login import UserMixin
from datetime import datetime, timezone


class User(db.Model, UserMixin):
    id= db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(150),unique=True,nullable=False)
    password= db.Column(db.String(255),nullable=False)
    email= db.Column(db.String(255),unique=True,nullable=False)
    profile_picture= db.Column(db.String(255),nullable=True)

    def __repr__(self):
        return f'<User: {self.username} Email: {self.email}>'
    def get_id(self):
        return self.id    