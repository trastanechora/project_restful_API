import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, request, marshal
from . import *
import requests

bp_song = Blueprint('song', __name__)
api = Api(bp_song)
class SongResource(Resource):
    wio_host = 'http://ws.audioscrobbler.com/2.0/'
    wio_apikey = '27f9a43dd663f505b4e03d41db4d4d51'

    def get(self, id=None):
        if id is None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=5)
            parser.add_argument('genre', location='args')
            parser.add_argument('artist', location='args')
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            qry = Songs.query

            if args['genre'] is not None:
                qry = qry.filter_by(title=args['genre'])

            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Songs.response_fields))
            return marshal(rows, Songs.response_fields), 200, { 'Content-Type': 'application/json' }
        
        else:
            qry = Songs.query.get(id)
            if qry is not None:
                return marshal(qry, Songs.response_fields), 200, { 'Content-Type': 'application/json' }
            else:
                return "Data Not Found", 200, { 'Content-Type': 'application/json' }

    def delete(self, id):
        qry = Songs.query.get(id)
        if qry is not None:
            db.session.delete(qry)
            db.session.commit()
            return "Data Deleted", 200, { 'Content-Type': 'application/json' }
        else :
            return "Data Not Found", 404, { 'Content-Type': 'application/json' }

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('title', location='json', required=True)
        parser.add_argument('artist', location='json', required=True)
        parser.add_argument('genre', location='json', required=True)
        args = parser.parse_args()

        qry = Songs.query.get(id)
        if qry is not None:  
            qry.title=args['title']
            qry.artist=args['artist']
            qry.genre=args['genre']    
            db.session.commit()
            return marshal(qry, Songs.response_fields), 200, { 'Content-Type': 'application/json' }
        else :
            return "Data Not Found", 404, { 'Content-Type': 'application/json' }

    def post(self):
        qry = Songs.query
        for data in qry:
            db.session.delete(data)
            db.session.commit()
        parser = reqparse.RequestParser()
        parser.add_argument('method', location='args', default=None)
        parser.add_argument('tag', location='args', default=None)
        parser.add_argument('format', location='args', default=None)

        args = parser.parse_args()
        list_genre = ["rock", "electronic", "seen live", "alternative", "indie", "pop", "female vocalists", "metal", "alternative rock", "jazz", "classic rock", "ambient", "experimental", "folk", "punk", "indie rock", "hard rock", "Hip-Hop", "instrumental", "singer-songwriter", "black metal", 	"dance", "80s", "Progressive rock", "death metal", "heavy metal", "hardcore", "british", "soul", "chillout", "electronica", "Classical", "industrial", "Soundtrack", "rap", "blues", "punk rock", "thrash metal", "90s", "acoustic", "metalcore", "psychedelic", "post-rock", "Progressive metal", "german", "funk", "hip hop", "new wave", "trance"]
        for genre in list_genre :
            rq = requests.get(self.wio_host, params={'method': args['method'], 'tag' : genre, 'format' : args['format'], 'api_key': self.wio_apikey})
            song = rq.json()
            for data in song['tracks']['track']:
                songs = Songs(None, data['name'], data['artist']['name'], genre)
                db.session.add(songs)
                db.session.commit()
        return marshal(songs, Songs.response_fields), 200, { 'Content-Type': 'application/json' }

class SongResourceAdmin(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', location='json', required=True)
        parser.add_argument('artist', location='json', required=True)
        parser.add_argument('genre', location='json', required=True)
        args = parser.parse_args()

        song = Songs(None, args['title'], args['artist'], args['genre'])
        db.session.add(song)
        db.session.commit()

        return marshal(song, Songs.response_fields), 200, { 'Content-Type': 'application/json' }


api.add_resource(SongResource, '/song', '/song/<int:id>')
api.add_resource(SongResourceAdmin, '/admin')


