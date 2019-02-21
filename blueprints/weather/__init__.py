import requests
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
import json

bp_weather = Blueprint('weather', __name__)
api = Api(bp_weather)

class PublicGetCurrentWeather(Resource):
    wio_host = "https://api.weatherbit.io/v2.0"
    wio_apikey = '001de4440e814c16bc45197fd601ef9d'

    # @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', location='args', default=None)
        args = parser.parse_args()

        rq = requests.get(self.wio_host + '/ip', params={'ip':args['ip'], 'key': self.wio_apikey})
        geo = rq.json()


        # send_url = 'http://freegeoip.net/json'
        # r = requests.get(send_url)
        # j = json.loads(r.text)
        # # lat = j['latitude']
        # # lon = j['longitude']
        # print(r)
        # print(j)

        lat = geo['latitude']
        lon = geo['longitude']
        print(lat)
        print(lon)
        rq = requests.get(self.wio_host + '/current', params={'lat': lat, 'lon': lon, 'key': self.wio_apikey})
        current = rq.json()

        # return {
        #     'kota': geo['city'],
        #     'organisasi': geo['organization'],
        #     'zona_waktu': geo['timezone'],
        #     'cuaca_sekarang': {
        #         'tanggal': current['data'][0]['datetime'],
        #         'temperatur': current['data'][0]['temp']
        #     }
        # }
        return current

api.add_resource(PublicGetCurrentWeather, '')