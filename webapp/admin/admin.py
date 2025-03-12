from flask import Blueprint, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound

admin_bp = Blueprint(
    'admin_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/admin_bp',
)

@admin_bp.route('/')
def admin_home():
    try:
        return render_template(f'admin/dashboard.html')
    except TemplateNotFound:
        abort(404)

@admin_bp.route('/dashboard')
def redirect_admin_home():
    return redirect(url_for('admin_bp.admin_home'))

@admin_bp.route('/login')
def admin_login():
    return render_template(f'admin/login.html')