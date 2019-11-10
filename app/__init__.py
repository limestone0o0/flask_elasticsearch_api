from flask import Flask
from flask_wtf import csrf
from flask_sqlalchemy import SQLAlchemy

import pymysql
pymysql.install_as_MySQLdb()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Develop')
    db.init_app(app)
    csrf.CSRFProtect(app)

    return app
