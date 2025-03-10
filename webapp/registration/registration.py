# use flask-wtf
from flask import Blueprint, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound


registration_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/main_bp',
)

