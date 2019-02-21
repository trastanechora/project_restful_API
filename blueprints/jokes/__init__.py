import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from blueprints import db
from flask_jwt_extended import jwt_required
import requests
from . import *

bp_jokes = Blueprint('jokes', __name__)
api = Api(bp_jokes)

class GetJokes(Resource):
    wio_host = 'https://official-joke-api.appspot.com'

    # @jwt_required
    def get(self):
        
        rq = requests.get(self.wio_host + '/random_joke')
        joke = rq.json()

        return {
            'joke': joke['setup']+joke['punchline']
        }

api.add_resource(GetJokes, '')
