from jinja2 import TemplateNotFound
import os
from db import db
from admin.models import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import PasswordField

from flask import Blueprint, render_template, abort, redirect, url_for, request, session, current_app, flash, jsonify
from jinja2 import TemplateNotFound

import pytz, json

JAKARTA_TZ = pytz.timezone('Asia/Jakarta')
ROLE_CHOICES = ["admin", "super_admin"]

COMPETITION_CHOICES = [
    "mini-soccer",
    "basket-putra",
    "basket-putri",
    "voli-putra",
    "voli-putri",
    "bulu-tangkis",
    "pencak-silat",
    "tenis-meja",
    "modern-dance",
    "band",
    "catur",
    "fotografi",
    "taekwondo",
    "english-debate",
    "short-movie",
    "wall-climbing",
    "cubing",
    "debat",
    "cerdas-cermat",
    "paduan-suara",
    "drama-modern",
    "digital-painting",
    "orasi",
]

admin_bp = Blueprint(
    'admin_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/admin_bp',
)

# Basic admin login & logout handler
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    # Get the client's IP address
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    if request.method == "POST":
        mongo_main = current_app.extensions['mongo_main']
        collection = mongo_main.db.admin_user
        
        username = request.form.get("username")
        password = request.form.get("password")
        user_data = collection.find_one({"username": username})

        if user_data and check_password_hash(user_data['password'], password):
            # session['user'] = serialize_document(user_data)
            #logging.info(f"Successful login by {username} from IP: {client_ip}")
            return redirect(url_for('admin_bp.index'))
        else:
            flash("Invalid username or password", "error")
            #logging.warning(f"Failed login attempt by {username} from IP: {client_ip}")

    return render_template("admin/login.html")

@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin_bp.login'))

# Normal Admin Panel Pages
@admin_bp.route('/')
def redirect_home():
    return redirect(url_for('admin_bp.home'))

@admin_bp.route('/panel/')
def home():
    user = session.get('user', {})
    if not user: return redirect(url_for('admin_bp.login'))
    return render_template("admin/dashboard.html")

@admin_bp.route('/profile')
def whoami():
    user = session.get('user', {})
    username = user.get('username', 'Guest')
    role = user.get('role', 'Unknown')
    return f"Username:{username}, Role: {role}"

@admin_bp.route('/panel/regis')
def admin_panel_regis():
    user = session.get('user', {})
    if not user: return redirect(url_for('admin_bp.login'))
    
    # mongo_main = current_app.extensions['mongo_main']
    # collection = mongo_main.db.users
    
    lomba = request.args.get('lomba')
    jenjang = request.args.get('jenjang')
    status = request.args.get('status')
    sort = request.args.get('sort', 'timestamp')
    
    query={}
    
    if lomba: query["regis_info.competition_id"] = lomba
    if jenjang:  query["regis_info.jenjang"] = jenjang
    if status:  query["regis_info.status"] = status
    
    # users = list(collection.find(query).sort(sort))
    # return render_template("admin/panel_regis.html", user=user, users=users, comp_choices=COMPETITION_CHOICES)
    return render_template("admin/panel_registration.html")

@admin_bp.route('/competition-status', methods=['GET'])
def competition_status():
    
    # Retrieve query parameters for filtering
    competition_id = request.args.get('competition_id')
    jenjang = request.args.get('jenjang')

    # Prepare query
    query = {}
    if competition_id:
        query["regis_info.competition_id"] = competition_id
    if jenjang:
        query["regis_info.jenjang"] = jenjang

    # mongo_main = current_app.extensions['mongo_main']
    # collection = mongo_main.db.users

    # Aggregation query to group by competition_id, jenjang, and status, and count the users in each status
    # pipeline = [
    #     {"$match": query},
    #     {
    #         "$group": {
    #             "_id": {
    #                 "competition_id": "$regis_info.competition_id",
    #                 "jenjang": "$regis_info.jenjang",
    #                 "status": "$regis_info.status"
    #             },
    #             "count": {"$sum": 1}
    #         }
    #     },
    #     {
    #         "$sort": {
    #             "_id.competition_id": 1,
    #             "_id.jenjang": 1,
    #             "_id.status": 1
    #         }
    #     }
    # ]

    # Execute the aggregation pipeline
    # results = list(collection.aggregate(pipeline))

    # Prepare the response data
    # response_data = {}
    # Initialize response_data with 0 counts for all statuses for every competition/jenjang pair
    # for competition_key, competition_data in competitions.items():
    #     comp_name = competition_data["name"]
    #     response_data[comp_name] = {}
    #     for jenjang_level in competition_data["jenjang"]:
    #         response_data[comp_name][jenjang_level] = {
    #             "Pending": 0,
    #             "Submitted": 0,
    #             "Confirmed": 0,
    #             "Waitlisted": 0,
    #             "Rejected": 0
    #         }
    # # Populate response_data with actual counts from the database
    # for result in results:
    #     comp_id = result['_id']['competition_id']
    #     jenjang_level = result['_id']['jenjang']
    #     status = result['_id']['status']
    #     count = result['count']

    #     # Find the competition name by competition_id
    #     for competition_key, competition_data in competitions.items():
    #         if competition_key == comp_id:
    #             comp_name = competition_data["name"]
    #             if jenjang_level in response_data[comp_name]:
    #                 response_data[comp_name][jenjang_level][status] = count

    # Render the results in the template
    # return render_template("admin/competition_status.html", data=response_data, competition_id=competition_id, jenjang=jenjang)
    return render_template("admin/competition_status.html")


# Super Admin(King👑) Pages
@admin_bp.route('/admins', methods=["GET"])
def get_admins():
    user = session.get('user', {})
    if not user: return redirect(url_for('admin_bp.login'))
    
    # admins = list(collection.find())
    # admins = [serialize_document(admin) for admin in admins]
    # return jsonify(admins), 200
    
@admin_bp.route('/admin/<username>')
def find_admin(username):
    user = session.get('user', {})
    if not user: return redirect(url_for('admin_bp.login'))
    
    # mongo_main = current_app.extensions['mongo_main']
    # collection = mongo_main.db.admin_user
    
    # query = {'username': username}
    # user = serialize_document(collection.find_one(query))
    
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

@admin_bp.route('/admin/<username>/update', methods=['PUT'])
def update_admin():
    user = session.get('user', {})
    role = user.get('role')
    if not user: return redirect(url_for('admin_bp.login'))
    pass

@admin_bp.route('/admin/<username>/delete', methods=["DELETE"])
def delete_admin():
    user = session.get('user', {})
    role = user.get('role')
    if not user: return redirect(url_for('admin_bp.login'))
    
    if role == 'super_admin':
        pass
        # mongo_main = current_app.extensions['mongo_main']
        # collection = mongo_main.db.admin_user
        # query = {'username': username}
        # result = collection.delete_one(query)
        # return jsonify({"deleted_count": result.deleted_count}), 200
    return redirect(url_for("admin_bp.dashboard"))

