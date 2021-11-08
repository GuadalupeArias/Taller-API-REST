import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS
from resources.auto import Auto, AutoId


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL2', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

#jwt = JWT(app, authenticate, identity) #/auth

api.add_resource(Auto, '/auto')
api.add_resource(AutoId, '/auto/<int:id>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
