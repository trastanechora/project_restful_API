import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from blueprints import db
from flask_jwt_extended import jwt_required, get_jwt_identity


from . import *

bp_client = Blueprint('client', __name__)
api = Api(bp_client)

class ClientResource(Resource):
    def __init__(self):
        if Clients.query.first() is None:
            clients = Clients(None, 'super_user', 'super_user0001', 'admin')
            db.session.add(clients)
            db.session.commit()

    @jwt_required
    def get(self, id=None):
        user = get_jwt_identity()
        identity = marshal(user, Clients.response_field)

        if identity['status'] == 'admin':
            if id == None:
                parse = reqparse.RequestParser()
                parse.add_argument('p',type=int,location='args',default=1)
                parse.add_argument('rp',type=int,location='args',default=5)
                parse.add_argument('client_id',location='args')
                parse.add_argument('status',location='args')
                
                args = parse.parse_args()

                offset = args['p']*args['rp']-args['rp']

                qry = Clients.query

                if args['client_id'] and args['status'] is not None:
                    qry = qry.filter(Clients.client_id.like("%"+args['client_id']+"%"))
                    qry = qry.filter_by(status=args['status'])
                elif args['client_id'] is not None and args['status'] is None:
                    qry = qry.filter(Clients.client_id.like("%"+args['client_id']+"%"))
                elif args['client_id'] is None and args['status'] is not None:
                    qry = qry.filter_by(status=args['status'])

                client_lists = []
                for client_list in qry.limit(args['rp']).offset(offset).all():
                    client_lists.append(marshal(client_list, Clients.response_field))
                return client_lists, 200, {'Content-Type': 'application/json'}
            else:
                qry = Clients.query.get(id)

                if qry is not None:
                    return marshal(qry, Clients.response_field)
                return {'status': 'NOT FOUND','message':'Client not found'}, 404, {'Content-Type':'application/json'}
        else:
            return 'UNAUTORIZED', 500, { 'Content-Type': 'application/json' }

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('client_key', location='json', required=True)
        parse.add_argument('client_secret', location='json', required=True)
        args = parse.parse_args()

        clients = Clients(None, args['client_key'], args['client_secret'], 'user')

        db.session.add(clients)
        db.session.commit()

        return marshal(clients, Clients.response_field), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def put(self, id):
        user = get_jwt_identity()
        identity = marshal(user, Clients.response_field)

        if identity['status'] == 'admin':
            parse = reqparse.RequestParser()
            parse.add_argument('client_key', location='json', required=True)
            parse.add_argument('client_secret', location='json', required=True)
            parse.add_argument('status', location='json', required=True)

            args = parse.parse_args()

            qry = Clients.query.get(id)
            if qry is None:
                return {'status': 'NOT FOUND','message':'Client not found'}, 404, {'Content-Type':'application/json'}
            else:    
                qry.client_key = args['client_key']
                qry.client_secret = args['client_secret']
                qry.status = args['status']

                db.session.commit()

                return marshal(qry, Clients.response_field), 200, {'Content-Type': 'application/json'}
        else:
            return 'UNAUTORIZED', 500, { 'Content-Type': 'application/json' }
            
    @jwt_required
    def delete(self, id):
        user = get_jwt_identity()
        identity = marshal(user, Clients.response_field)

        if identity['status'] == 'admin':
            qry = Clients.query.get(id)
            if qry is None:
                return {'status': 'NOT FOUND','message':'Client not found'}, 404, {'Content-Type':'application/json'}        
            else:
                db.session.delete(qry)
                db.session.commit()
                return ("Deleted")
        else:
            return 'UNAUTORIZED', 500, { 'Content-Type': 'application/json' }

api.add_resource(ClientResource,'')