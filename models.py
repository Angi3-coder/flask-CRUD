from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    

    @validates('username')
    def validates_username(self, key, username):
        if len(username)< 5:
            raise  ValueError ("Username must be atleast 5 characters")
        return username
        
    @validates('email')
    def validates_email(self, key, email):
        if '@' not in email:
            raise ValueError ("Invalid email address")
        
        return email


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content= db.Column(db.String(350), nullable=False)

    user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    