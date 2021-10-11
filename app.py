import os


from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.auto import Auto, AutoList, AutoId



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)


jwt = JWT(app, authenticate, identity) #/auth

api.add_resource(Auto, '/auto')
api.add_resource(AutoId, '/auto/<int:id>')
api.add_resource(AutoList, '/autos')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
