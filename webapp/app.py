from flask import Flask
from main.main import main_bp

app = Flask(__name__)
app.register_blueprint(main_bp)