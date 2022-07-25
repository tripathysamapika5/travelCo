from flask import Flask
from flask_cors import CORS
import os
import logging

from flask_sqlalchemy import SQLAlchemy



class AppFactory:

    basedir = os.path.dirname(os.path.abspath(__file__))
    BASE_URL = 'http://127.0.0.1:5000'

    @classmethod
    def getApp(cls, appName):
        app = Flask(appName,template_folder='templates')
        CORS(app, resources={r"/*": {"origins": "*"}})
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(AppFactory.basedir, 'database.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        BASE_URL = 'http://127.0.0.1:5000'
        app.secret_key = "secret key"
        app.config['UPLOAD_FOLDER'] = 'static/uploads'
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
        logging.info(app.config)
        return app



class DBFactory:

    @classmethod
    def getDb(cls):
        return SQLAlchemy(AppFactory.getApp("app"))


#########################
#######Constants#########
#########################
db = DBFactory.getDb()


