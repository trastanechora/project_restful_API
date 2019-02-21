import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from .. import *
from ..song import Songs

import requests

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_core = Blueprint('core', __name__)
api = Api(bp_core)

class CoreResources(Resource):
    wio_host = 'https://api.weatherbit.io/v2.0'
    wio_apikey = '001de4440e814c16bc45197fd601ef9d'

    category_1 = [
       "seen live",
       "female vocalists",
       "jazz",
       "classic rock",
       "ambient",
       "80s",
       "chillout",
       "acoustic",
    ]

    category_2 = [
        "singer-songwriter",
        "british", 
        "soul",
        "blues",
    ]

    category_3 = [
        "rock",
        "electronic",
        "alternative", 
        "indie", 
        "pop",
        "metal", 
        "alternative rock",
        "experimental", 
        "folk", 
        "punk", 
        "indie rock", 
        "hard rock", 
        "Hip-Hop", 
        "instrumental",
        "black metal",
        "dance",
        "Progressive rock", 
        "death metal", 
        "heavy metal", 
        "hardcore",
        "electronica",
        "Classical",
        "industrial", 
        "Soundtrack", 
        "rap",
        "punk rock", 
        "thrash metal", 
        "90s",
        "metalcore", 
        "psychedelic",
        "post-rock", 
        "Progressive metal", 
        "german", 
        "funk", 
        "hip hop", 
        "new wave", 
        "trance"
    ]

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', location='args', default=None)
        args = parser.parse_args()

        rq = requests.get(self.wio_host + '/ip', params={'ip': args['ip'],'key': self.wio_apikey})
        geo = rq.json()
        
        lat = geo['latitude']
        lon = geo['longitude']
        rq = requests.get(self.wio_host + '/current', params={'lat': lat, 'lon': lon,'key': self.wio_apikey})
        current = rq.json()

        weather_code = int(current['data'][0]['weather']['code'])



        # return {
        #     'country_code': current['data'][0]['country_code'],
        #     'city_name': current['data'][0]['city_name'],
        #     'weather_code': current['data'][0]['weather']['code'],
        #     'weather_desc': current['data'][0]['weather']['description'],
        #     'temp': current['data'][0]['temp']
        # }
        # return int(current['data'][0]['weather']['code'])

        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=5)
        # parser.add_argument('name', type=str, location='args')
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Songs.query

        # if args['name'] is not None:
        #     qry = qry.filter(Books.book_title.like("%"+args['name']+"%"))
        
        qry = qry.filter_by(genre = "pop")
        rows = []
        # print(args)
        # print(offset)
        for row in qry.all():
            # if row.book_status == "Show":
            #     rows.append(marshal(row, Books.response_field))
            rows.append(marshal(row, Songs.response_fields))
        
        return rows, 200, { "content-type": "application/json" }

api.add_resource(CoreResources, '')