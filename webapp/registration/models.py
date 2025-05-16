import os
from db import db
from datetime import datetime
from werkzeug.utils import secure_filename

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    team_size = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # File paths
    statement_path = db.Column(db.String(255), nullable=False)
    school_permission_path = db.Column(db.String(255), nullable=False)
    nisn_path = db.Column(db.String(255), nullable=False)
    student_card_path = db.Column(db.String(255), nullable=False)
    selfie_path = db.Column(db.String(255), nullable=False)
    photo_path = db.Column(db.String(255), nullable=False)
    birth_certificate_path = db.Column(db.String(255), nullable=False)
    report_card_path = db.Column(db.String(255), nullable=False)
    non_athlete_statement_path = db.Column(db.String(255), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def save_uploaded_file(file, upload_folder, allowed_extensions=None):
        if file.filename == '':
            return None
            
        if allowed_extensions:
            ext = os.path.splitext(file.filename)[1].lower()
            if ext not in allowed_extensions:
                return None
                
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return file_path

    def __repr__(self):
        return f'<User {self.full_name} - {self.school}>'
