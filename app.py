from flask import Flask
from flask_restful import Api
from flask_restful_swagger import swagger
from flask_jwt import JWT
import os
import models
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from resources.users import Users, LoginUsers



app = Flask(__name__)

db = models.db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/cluzzchef'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kmnorth007:kmnorth007@kmnorth.crx51qhsnwjl.us-east-2.rds.amazonaws.com:3306/cluzzchef'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'akshay7272'
api = Api(app)
api = swagger.docs(Api(app), apiVersion='0.1')



migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


api.add_resource(Users, '/register')
api.add_resource(LoginUsers, '/login/<string:phone_number>/<string:password>')



if __name__ == '__main__':
	# from db import db
	db.init_app(app) 
	manager.run()