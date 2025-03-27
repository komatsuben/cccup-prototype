from flask import Blueprint, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/main_bp',
)

@main_bp.route('/')
def home():
    try:
        return render_template(f'main/landing.html')
    except TemplateNotFound:
        abort(404)

@main_bp.route('/landing')
def redirect_landing():
    return redirect(url_for('main_bp.home'))

@main_bp.route('/comingsoon')
def comingsoon():
    return render_template('main/comingsoon.html')

@main_bp.route('/merchandise')
def merchandise():
    return render_template('main/merch.html')

@main_bp.route('/test')
def boilerplate():
    return render_template('main/tests.html')