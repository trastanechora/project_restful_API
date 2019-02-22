import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from .. import *
from ..song import Songs
from ..news.resources import *
from ..jokes import *
import random

import requests

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_core = Blueprint('core', __name__)
api = Api(bp_core)

class CoreResources(Resource):
    wio_host = 'https://api.weatherbit.io/v2.0'
    wio_apikey = '001de4440e814c16bc45197fd601ef9d'

    category_1 = [
       "seen live", "female vocalists", "jazz", "classic rock", "ambient", "80s", "chillout", "acoustic",
    ]

    category_2 = [
        "singer-songwriter", "british", "soul", "blues",
    ]

    category_3 = [
        "rock", "electronic", "alternative", "indie", "pop", "metal", "alternative rock", "experimental", "folk", "punk", "indie rock", "hard rock", "Hip-Hop", "instrumental", "black metal", "dance", "Progressive rock", "death metal", "heavy metal", "hardcore", "electronica", "Classical", "industrial", "Soundtrack", "rap", "punk rock", "thrash metal", "90s", "metalcore", "psychedelic", "post-rock", "Progressive metal", "german", "funk", "hip hop", "new wave", "trance"
    ]

    def get_recomend_music(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', location='args', default=None)
        args = parser.parse_args()

        rq = requests.get(self.wio_host + '/ip', params={'ip': args['ip'],'key': self.wio_apikey})
        geo = rq.json()
        
        lat = geo['latitude']
        lon = geo['longitude']
        rq = requests.get(self.wio_host + '/current', params={'lat': lat, 'lon': lon,'key': self.wio_apikey})
        weather = rq.json()
        current = {
            'timezone' : weather['data'][0]['timezone'],
            'clouds' : weather['data'][0]['clouds'],
            'datetime' : weather['data'][0]['datetime'],
            'city' : weather['data'][0]['city_name'],
            'weather' : weather['data'][0]['weather']['description'],
            'temp' : weather['data'][0]['temp']
        }

        self.current = current

        weather_code = int(weather['data'][0]['weather']['code'])

        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=5)
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Songs.query

        result = []
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Songs.response_fields))

        if weather_code <= 600:
            test2 = []
            for genre in self.category_1:
                test = qry.filter_by(genre = genre)
                for row in test.limit(args['rp']).offset(offset).all():
                    test2.append(marshal(row, Songs.response_fields))
        elif weather_code > 600 and weather_code < 800:
            test2 = []
            for genre in self.category_2:
                test = qry.filter_by(genre = genre)
                for row in test.limit(args['rp']).offset(offset).all():
                    test2.append(marshal(row, Songs.response_fields))
        else:
            test2 = []
            for genre in self.category_3:
                test = qry.filter_by(genre = genre)
                for row in test.limit(args['rp']).offset(offset).all():
                    test2.append(marshal(row, Songs.response_fields))

        output = []
        while len(output) < 10:
            temp = random.choice(test2)
            if temp not in output:
                output.append(temp)
        
        return {'RECOMENDED_SONGS': output}

    def get_news_list(self):
        news = PublicGetNews.get(PublicGetNews)
        list_news = []
        for data in news :
            filtered_news = {
                'publisher' : news[0]['publisher'],
                'title' : news[0]['title'],
                'description' : news[0]['description'],
                'author' : news[0]['author'],
                'published_at' : news[0]['published_at'],
                'content' : news[0]['content'],
                'url' : news[0]['url']
            } 
            list_news.append(filtered_news)
        return {'TOPNEWS': list_news}

    def get_joke_list(self):
        jokes = GetJokes.get(GetJokes)
        return jokes

    @jwt_required
    def get(self):
        result = []
        news = self.get_news_list()
        jokes = self.get_joke_list()
        songs = self.get_recomend_music()
        result.append({'WEATHER_CONDITION': self.current})
        result.append(songs)
        result.append(jokes)
        result.append(news)
        return result
        

api.add_resource(CoreResources, '')