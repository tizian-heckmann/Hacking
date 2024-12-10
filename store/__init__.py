from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.jinja_env.autoescape = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://dbuser1:7M1BtbB7m1NfBETaBbf85H2H@192.168.2.177:3306/gamestoredb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "super-secret"

THUMBNAIL_UPLOAD_DIRECTORY = "/home/tizian/hochschule_albstadt-sigmaringen/hacking_mit_python/gamestore/store/static/resources/img/"

db = SQLAlchemy(app)

from store import routes
