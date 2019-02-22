import requests
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
import json
import requests
from . import News
from .. import db

bp_news = Blueprint('news', __name__)
api = Api(bp_news)

class PublicGetNews(Resource):
    base_url = "https://newsapi.org/v2/top-headlines"
    key = "995ea15a75714a0496b4befa6ae915ef"

    # @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=5)
        parser.add_argument('name', type=str, location='args')
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = News.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, News.response_field))
        
        return rows, 200, { "content-type": "application/json" }

    # @jwt_required
    def post(self):
        qry = News.query
        for data in qry:
            db.session.delete(data)
            db.session.commit()
        country_list = ['ar', 'au', 'be', 'ca', 'ch', 'co', 'de', 'fr', 'gb', 'id', 'ie', 'it', 'mx', 'nl', 'no', 'nz', 'pt', 'se', 'sg', 'us']
        for country in country_list:
            req = requests.get(self.base_url, params={'country': country, 'apiKey': self.key})
            result = req.json()

            total_news = result["totalResults"]

            for news in result['articles']:
                temp = {
                    'publisher': news['source']['name'],
                    'title': news['title'],
                    'description': news['description'],
                    'author': news['author'],
                    'published_at': news['publishedAt'],
                    'content': news['content'],
                    'url': news['url'],
                    'country': country
                }

                berita = News(None, temp['publisher'], temp['title'], temp['description'], temp ['author'], temp['published_at'], temp['content'], temp['url'], temp['country'])
                db.session.add(berita)

        db.session.commit()
        return "OK", 200, { "content-type": "application/json" }

api.add_resource(PublicGetNews, '')