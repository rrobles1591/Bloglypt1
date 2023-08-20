import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__="User"

    def __repr__(self):
        p= self
        return f"<User id={p.id} first_name={p.first_name} last_name={p.last_name} image_url={p.image_url}>"

    id = db.Column(db.Integer,
                   primary_key=True, 
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=(False))

    image_url = db.Column(db.Text)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    #To create database with this model (ipython %run
    #  app.py, db.create_all() )

class Post (db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    # @property
    # def friendly_date(self):
    #     return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")