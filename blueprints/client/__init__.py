import random, logging
from blueprints import db
from flask_restful import fields

class Clients(db.Model):
    __tablename__ = "client"
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_key = db.Column(db.String(50))
    client_secret = db.Column(db.String(50))
    status = db.Column(db.String(50))

    response_field = {
        'client_id' : fields.Integer,
        'client_key' : fields.String,
        'client_secret' : fields.Integer,
        'status' : fields.String,
    }

    def __init__(self, client_id, client_key, client_secret, status):
        self.client_id = client_id
        self.client_key = client_key
        self.client_secret = client_secret
        self.status = status

    def __repr__(self):
        return '<Client id %d>' % self.client_id
