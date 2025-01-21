from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import dotenv_values
from datetime import timedelta


app = Flask(__name__)

app.jinja_env.autoescape = True

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://dbuser1:7M1BtbB7m1NfBETaBbf85H2H@192.168.2.177:3306/gamestoredb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret"


THUMBNAIL_UPLOAD_DIRECTORY = "/home/tizian/hochschule_albstadt-sigmaringen/hacking_mit_python/gamestore/store/static/resources/img/"

DAYS_TO_EXPIRATION: int = 28
JWT_CLEANUP_INTERVAL_SECONDS: int = 600
dotenv_configuration: dict[str, str] = dotenv_values()

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=DAYS_TO_EXPIRATION)
app.config["JWT_SECRET_KEY"] = dotenv_configuration["JWT_SECRET_KEY"]
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token_cookie"

# GET is not included by default but one can never be sure that a developer does not implement side
# effects in a GET request which would make it relevant for csrf.
app.config["JWT_CSRF_METHODS"] = ["POST", "PUT", "PATCH", "DELETE"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_COOKIE_SAMESITE"] = "Strict"
app.config["JWT_COOKIE_SECURE"] = False  # use this as soon as certificates are in place
app.config["JWT_ACCESS_CSRF_COOKIE_NAME"] = "csrf_access_token"

db = SQLAlchemy(app)
jwt = JWTManager(app)

from store import routes
