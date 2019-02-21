from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json, logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager
from datetime import timedelta

# ================== Declare Flask into app =====================
app = Flask(__name__)
api = Api(app, catch_all_404s=True)
# ===============================================================

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@0.0.0.0:3306/project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'SFhewoihewg870923ugsihgh3298hgoisdghsiueg32gMAE'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return identity

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# ================ Declare app to record log ====================
@app.after_request
def after_request(response):
    if request.method == "GET":
        app.logger.warning("REQUEST LOG\t%s", json.dumps(
            {"request": request.args.to_dict(), "response": json.loads(response.data.decode('utf-8'))}
            ))
    else:
        app.logger.warning("REQUEST LOG\t%s", json.dumps(
            {"request": request.get_json(), "response": json.loads(response.data.decode('utf-8'))}
            ))
    return response
# ================================================================

# ================ Import and register Blueprint =================
from blueprints.auth import bp_auth
from blueprints.weather import bp_weather
from blueprints.news import bp_news
from blueprints.song.resources import bp_song


app.register_blueprint(bp_auth, url_prefix='/auth')
app.register_blueprint(bp_weather, url_prefix='/weather')
app.register_blueprint(bp_news, url_prefix='/news')
app.register_blueprint(bp_song)
# ================================================================

db.create_all()


