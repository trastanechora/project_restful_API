from flask_restful import fields
from blueprints import db

class Songs(db.Model):
    __tablename__ = "song"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    genre = db.Column(db.String(100))

    response_fields = {
            'id': fields.Integer,
            'title': fields.String,
            'artist': fields.String,
            'genre' : fields.String
    }

    def __init__(self, id, title, artist, genre):
        self.id = id
        self.title = title
        self.artist = artist
        self.genre = genre


    def __repr__(self) :
        return'<%r>'%self.title
    