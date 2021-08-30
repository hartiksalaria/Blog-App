from flask_login import UserMixin
from . import db
import datetime


def get_time():
    now = datetime.datetime.now()
    exact_time = now.strftime("%Y-%m-%d %H:%M")
    return exact_time


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(50), nullable=False, default="default.png")
    post_id = db.relationship('Post', backref='user', lazy=True)

    def __repr__(self):
        return self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(50), nullable=False, default=get_time())
    title = db.Column(db.String(120), nullable=False)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_id = db.relationship('Comment', backref='post', lazy=True)

    def __repr__(self):
        return self.title


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(50), nullable=False, default=get_time())
    comment_content = db.Column(db.String(500), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return self.author