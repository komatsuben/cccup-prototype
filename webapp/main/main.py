from flask import Blueprint, render_template, abort, redirect, url_for, flash, request
from jinja2 import TemplateNotFound
from .forms import LoginForm

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

@main_bp.route('/competition')
def competition():
    return render_template('main/competition.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Add your authentication logic here
        username = form.username.data
        password = form.password.data
        # TODO: Add actual user authentication
        flash('Login successful!', 'success')
        return redirect(url_for('main_bp.home'))
    return render_template('main/login.html', form=form)