# blueprints/examples.py

from flask import Blueprint, request, jsonify, current_app, render_template
from werkzeug.utils import secure_filename
from bson import ObjectId
from datetime import datetime
import digitalocean
import os

examples_bp = Blueprint('examples', __name__, template_folder='templates')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Utility function to convert MongoDB documents to JSON serializable format
def serialize_document(doc):
    doc['_id'] = str(doc['_id'])
    return doc

# Find all users
@examples_bp.route('/users', methods=['GET'])
def find_users():
    mongo_main = current_app.extensions['mongo_main']
    collection = mongo_main.db.users
    users = list(collection.find())
    users = [serialize_document(user) for user in users]
    return jsonify(users), 200

# Insert a new user
@examples_bp.route('/users', methods=['POST'])
def insert_user():
    mongo_main = current_app.extensions['mongo_main']
    collection = mongo_main.db.users
    user_data = request.json
    # Set required fields
    required_fields = ['name', 'email', 'phone', 'password']
    for field in required_fields:
        if field not in user_data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    user_data['user_type'] = "Participant"

    # Set default values for nested fields
    user_data['regis_info'] = user_data.get('regis_info', {
        "registration_time": datetime.now(),
        "teamname": "",
        "school": "",
        "competition_id": "",
        "jenjang": "",
        "subkategori": "",
        "status": "Pending"
    })

    user_data['regis_files'] = user_data.get('regis_files', {
        "pernyataan_filename": "",
        "izinsekolah_filename": "",
        "nisn_filename": "",
        "kartupelajar_filename": "",
        "selfie_filename": "",
        "pasfoto_filename": ""
    })

    user_data['other_info'] = user_data.get('other_info', {
        "lagu_wajib": "",
        "lagu_bebas": "",
        "judul_film": ""
    })

    user_data['members'] = user_data.get('members', [])

    result = collection.insert_one(user_data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201

# Update a user
@examples_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    mongo_main = current_app.extensions['mongo_main']
    collection = mongo_main.db.users
    query = {'user_id': user_id}
    update_data = {'$set': request.json}
    result = collection.update_one(query, update_data)
    return jsonify({"matched_count": result.matched_count, "modified_count": result.modified_count}), 200

# Delete a user
@examples_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    mongo_main = current_app.extensions['mongo_main']
    collection = mongo_main.db.users
    query = {'user_id': user_id}
    result = collection.delete_one(query)
    return jsonify({"deleted_count": result.deleted_count}), 200

# Find members by user ID
@examples_bp.route('/users/<user_id>/members', methods=['GET'])
def find_members_by_user(user_id):
    mongo_main = current_app.extensions['mongo_main']
    collection = mongo_main.db.users
    user = collection.find_one({'user_id': user_id})
    if user:
        members = user.get('members', [])
        return jsonify([serialize_document(member) for member in members]), 200
    return jsonify({"error": "User not found"}), 404

# Insert a member to a user
@examples_bp.route('/users/<user_id>/members', methods=['POST'])
def insert_member(user_id):
    mongo_main = current_app.extensions['mongo_main']
    collection = mongo_main.db.users
    member_data = request.json

    # Generate a new ObjectId for the member
    member_data['_id'] = ObjectId()

    query = {'user_id': user_id}
    update = {'$push': {'members': member_data}}
    result = collection.update_one(query, update)
    if result.matched_count > 0:
        return jsonify({"inserted_member_id": str(member_data['_id'])}), 201
    return jsonify({"error": "User not found"}), 404

# Update a member of a user
@examples_bp.route('/users/<user_id>/members/<member_id>', methods=['PUT'])
def update_member(user_id, member_id):
    mongo_main = current_app.extensions['mongo_main']
    collection = mongo_main.db.users
    query = {'user_id': user_id, 'members._id': ObjectId(member_id)}
    update_data = {'$set': {f'members.$.{key}': value for key, value in request.json.items()}}
    result = collection.update_one(query, update_data)
    return jsonify({"matched_count": result.matched_count, "modified_count": result.modified_count}), 200

# Delete a member of a user
@examples_bp.route('/users/<user_id>/members/<member_id>', methods=['DELETE'])
def delete_member(user_id, member_id):
    mongo_main = current_app.extensions['mongo_main']
    collection = mongo_main.db.users
    query = {'user_id': user_id}
    update = {'$pull': {'members': {'user_id': ObjectId(member_id)}}}
    result = collection.update_one(query, update)
    return jsonify({"modified_count": result.modified_count}), 200

@examples_bp.route('/upload', methods=['GET'])
def form_file():
    # Render the upload form
    return render_template('examples/upload.html')

@examples_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Secure the filename
        filename = secure_filename(file.filename)

        # Create a temporary file path to save the uploaded file
        temp_file_path = os.path.join('/tmp', filename)
        file.save(temp_file_path)

        # Upload to DigitalOcean Spaces
        try:
            spaces_client = current_app.extensions['spaces_client']
            space_name = current_app.config['SPACES_NAME']
            space_folder = current_app.config['SPACES_FOLDER']

            # Define where to save the file in the space (in the "testing" folder)
            save_as = f"uploads/{filename}"

            # Upload the file using the utility function
            digitalocean.upload_file_to_space(
                spaces_client,
                space_folder,
                temp_file_path,
                save_as,
                is_public=True
            )

            # Construct the file URL
            file_url = f"https://{space_name}.{current_app.config['SPACES_REGION_NAME']}.digitaloceanspaces.com/{space_folder}/{save_as}"

            file_data = {
                "filename": filename,
                "url": file_url,
                "folder": "testing"
            }
            mongo_main = current_app.extensions['mongo_main']
            result = mongo_main.db.files.insert_one(file_data)

            # Clean up the temporary file
            os.remove(temp_file_path)

            return jsonify({"file_id": str(result.inserted_id), "url": file_url}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Invalid file type"}), 400

@examples_bp.route('/files', methods=['GET'])
def list_files():
    mongo_main = current_app.extensions['mongo_main']
    files = list(mongo_main.db.files.find())
    for file in files:
        file['_id'] = str(file['_id'])
    return jsonify(files), 200

@examples_bp.route('/files/<file_id>', methods=['GET'])
def get_file(file_id):
    mongo_main = current_app.extensions['mongo_main']
    file = mongo_main.db.files.find_one({"_id": ObjectId(file_id)})
    if file:
        file['_id'] = str(file['_id'])
        return jsonify(file), 200
    return jsonify({"error": "File not found"}), 404