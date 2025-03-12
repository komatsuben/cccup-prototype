from flask import Flask
from main.main import main_bp
from admin.admin import admin_bp
from registration.registration import registration_bp

app = Flask(__name__)

app.register_blueprint(admin_bp, url_prefix="/admin") #
app.register_blueprint(main_bp, url_prefix="/")
app.register_blueprint(registration_bp, url_prefix="/register")