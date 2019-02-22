import requests
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
import json
import requests
from . import News
from .. import db
from ..client import Clients

bp_news = Blueprint('news', __name__)
api = Api(bp_news)

class PublicGetNews(Resource):
    base_url = "https://newsapi.org/v2/top-headlines"
    key = "995ea15a75714a0496b4befa6ae915ef"

    @jwt_required
    def get(self):
        qry = News.query

        rows = []

        user = get_jwt_identity()
        identity = marshal(user, Clients.response_field)

        if identity['status'] == 'user' or 'admin':
            for row in qry.all():
                rows.append(marshal(row, News.response_field))

            return rows
        else:
            return 'UNAUTORIZED', 500, { 'Content-Type': 'application/json' }

    @jwt_required
    def post(self):
        qry = News.query
        for data in qry:
            db.session.delete(data)
            db.session.commit()
        
        user = get_jwt_identity()
        identity = marshal(user, Clients.response_field)

        if identity['status'] == 'admin':
            req = requests.get(self.base_url, params={'country': 'id', 'apiKey': self.key})
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
                    'country': 'id'
                }
                berita = News(None, temp['publisher'], temp['title'], temp['description'],temp ['author'], temp['published_at'], temp['content'], temp['url'], temp['country'])
                db.session.add(berita)
                db.session.commit()
            return "OK", 200, { "content-type": "application/json" }
        else:
            return 'UNAUTORIZED', 500, { 'Content-Type': 'application/json' }

api.add_resource(PublicGetNews, '')