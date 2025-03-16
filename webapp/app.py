import os
from flask import Flask
from flask_migrate import Migrate
# blueprints
from main.main import main_bp
from registration.registration import registration_bp
from admin.admin import admin_bp
from matches.matches import matches_bp
import psycopg2

from matches.models import Match

from db import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DEVELOPMENT_DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(main_bp, url_prefix="/")
app.register_blueprint(registration_bp, url_prefix="/register")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(matches_bp, url_prefix="/matches")