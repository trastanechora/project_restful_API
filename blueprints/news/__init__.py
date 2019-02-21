import random
from .. import db
from flask_restful import fields

class News(db.Model):
    __tablename__ = "News"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    publisher = db.Column(db.String(255))
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    author = db.Column(db.String(255))
    published_at = db.Column(db.String(255))
    content = db.Column(db.String(1000))
    url = db.Column(db.String(255))

    response_field = {
        'id': fields.Integer,
        'publisher': fields.String,
        'title': fields.String,
        'description': fields.String,
        'author': fields.String,
        'published_at': fields.String,
        'content': fields.String,
        'url': fields.String
    }

    def __init__(self, id, publisher, title, description, author, published_at, content, url):
        self.id = id
        self.publisher = publisher
        self.title = title
        self.description = description
        self.author = author
        self.published_at = published_at
        self.content = content
        self.url = url

    def __repr__(self):
        return '<News %r>' % self.id