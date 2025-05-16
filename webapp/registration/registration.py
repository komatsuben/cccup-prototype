import os
from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash
from db import db
from .models import User
from .forms import RegistrationForm

registration_bp = Blueprint(
    'registration_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/registration_bp',
)

def ensure_upload_dir():
    """Ensure upload directory exists"""
    upload_dir = os.path.join(current_app.root_path, 'uploads')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return upload_dir

@registration_bp.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            upload_dir = ensure_upload_dir()
            user_dir = os.path.join(upload_dir, form.email.data.replace('@', '_'))
            os.makedirs(user_dir, exist_ok=True)
            
            # Save uploaded files
            def save_file(field, allowed_extensions=None):
                if field.data:
                    return User.save_uploaded_file(
                        field.data, 
                        user_dir,
                        allowed_extensions
                    )
                return None
            
            # Save all files
            statement_path = save_file(form.statement, ['pdf'])
            school_permission_path = save_file(form.school_permission, ['pdf'])
            nisn_path = save_file(form.nisn, ['png', 'jpg', 'jpeg', 'pdf'])
            student_card_path = save_file(form.student_card, ['png', 'jpg', 'jpeg'])
            selfie_path = save_file(form.selfie, ['png', 'jpg', 'jpeg'])
            photo_path = save_file(form.photo, ['png', 'jpg', 'jpeg'])
            birth_certificate_path = save_file(form.birth_certificate, ['png', 'jpg', 'jpeg', 'pdf'])
            report_card_path = save_file(form.report_card, ['png', 'jpg', 'jpeg', 'pdf'])
            non_athlete_statement_path = save_file(form.non_athlete_statement, ['pdf'])
            
            # Create new user
            new_user = User(
                full_name=form.full_name.data,
                school=form.school.data,
                team_size=form.team_size.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
                statement_path=statement_path,
                school_permission_path=school_permission_path,
                nisn_path=nisn_path,
                student_card_path=student_card_path,
                selfie_path=selfie_path,
                photo_path=photo_path,
                birth_certificate_path=birth_certificate_path,
                report_card_path=report_card_path,
                non_athlete_statement_path=non_athlete_statement_path
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Pendaftaran berhasil! Silakan masuk dengan akun Anda.', 'success')
            return redirect(url_for('main_bp.login'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Registration error: {str(e)}')
            flash('Terjadi kesalahan saat mendaftar. Silakan coba lagi.', 'error')
    
    return render_template('registration/form.html', form=form)