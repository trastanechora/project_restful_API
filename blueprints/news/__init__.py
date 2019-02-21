import requests
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
import json
import requests

bp_news = Blueprint('news', __name__)
api = Api(bp_news)

class PublicGetNews(Resource):
    # wio_host = "https://api.weatherbit.io/v2.0"
    # wio_apikey = '001de4440e814c16bc45197fd601ef9d'
    base_url = "https://newsapi.org/v2/top-headlines"
    key = "995ea15a75714a0496b4befa6ae915ef"

    # @jwt_required
    def get(self):
        req = requests.get(self.base_url, params={'country': 'ID', 'apiKey': self.key})
        result = req.json()

        total_news = result["totalResults"]
        list_news = []
        for news in result['articles']:
            temp = {
                'publisher': news['source']['name'],
                'title': news['title'],
                'description': news['description'],
                'author': news['author'],
                'published_at': news['publishedAt'],
                'content': news['content'][:-15],
                'url': news['url']
            }
            list_news.append(temp)
        return list_news

api.add_resource(PublicGetNews, '')