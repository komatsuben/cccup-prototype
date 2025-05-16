from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from .models import User
import os

class RegistrationForm(FlaskForm):
    # Personal Information
    full_name = StringField('Nama Lengkap', 
        validators=[
            DataRequired(message='Nama lengkap harus diisi'),
            Length(min=3, max=100, message='Panjang nama harus antara 3 sampai 100 karakter')
        ],
        render_kw={"placeholder": "Masukkan nama lengkap sesuai KTP/Kartu Pelajar"}
    )
    
    school = StringField('Asal Sekolah',
        validators=[
            DataRequired(message='Asal sekolah harus diisi'),
            Length(min=3, max=100, message='Panjang nama sekolah harus antara 3 sampai 100 karakter')
        ],
        render_kw={"placeholder": "Nama lengkap sekolah asal"}
    )
    
    team_size = IntegerField('Jumlah Anggota',
        validators=[
            DataRequired(message='Jumlah anggota harus diisi'),
            NumberRange(min=1, max=50, message='Jumlah anggota harus antara 1 sampai 50')
        ],
        render_kw={"placeholder": "Jumlah anggota dalam tim"}
    )
    
    email = StringField('Email', 
        validators=[
            DataRequired(message='Email harus diisi'),
            Email(message='Format email tidak valid')
        ],
        render_kw={"placeholder": "contoh@email.com"}
    )
    
    password = PasswordField('Kata Sandi', 
        validators=[
            DataRequired(message='Kata sandi harus diisi'),
            Length(min=8, message='Kata sandi minimal 8 karakter')
        ],
        render_kw={"placeholder": "Buat kata sandi yang kuat"}
    )
    
    confirm_password = PasswordField('Konfirmasi Kata Sandi', 
        validators=[
            DataRequired(message='Harap konfirmasi kata sandi Anda'),
            EqualTo('password', message='Kata sandi tidak cocok')
        ],
        render_kw={"placeholder": "Ketik ulang kata sandi"}
    )
    
    # File Uploads
    statement = FileField('Pernyataan (PDF)',
        validators=[
            FileRequired(message='File pernyataan harus diunggah'),
            FileAllowed(['pdf'], 'Hanya file PDF yang diizinkan')
        ]
    )
    
    school_permission = FileField('Izin Sekolah (PDF)',
        validators=[
            FileRequired(message='File izin sekolah harus diunggah'),
            FileAllowed(['pdf'], 'Hanya file PDF yang diizinkan')
        ]
    )
    
    nisn = FileField('NISN (PNG/JPG/JPEG/PDF)',
        validators=[
            FileRequired(message='File NISN harus diunggah'),
            FileAllowed(['png', 'jpg', 'jpeg', 'pdf'], 'Hanya file PNG, JPG, JPEG, atau PDF yang diizinkan')
        ]
    )
    
    student_card = FileField('Kartu Pelajar (PNG/JPG/JPEG)',
        validators=[
            FileRequired(message='File kartu pelajar harus diunggah'),
            FileAllowed(['png', 'jpg', 'jpeg'], 'Hanya file PNG, JPG, atau JPEG yang diizinkan')
        ]
    )
    
    selfie = FileField('Selfie (PNG/JPG/JPEG)',
        validators=[
            FileRequired(message='File selfie harus diunggah'),
            FileAllowed(['png', 'jpg', 'jpeg'], 'Hanya file PNG, JPG, atau JPEG yang diizinkan')
        ]
    )
    
    photo = FileField('Pas Foto (PNG/JPG/JPEG)',
        validators=[
            FileRequired(message='File pas foto harus diunggah'),
            FileAllowed(['png', 'jpg', 'jpeg'], 'Hanya file PNG, JPG, atau JPEG yang diizinkan')
        ]
    )
    
    birth_certificate = FileField('Akte Kelahiran (PNG/JPG/JPEG/PDF)',
        validators=[
            FileRequired(message='File akte kelahiran harus diunggah'),
            FileAllowed(['png', 'jpg', 'jpeg', 'pdf'], 'Hanya file PNG, JPG, JPEG, atau PDF yang diizinkan')
        ]
    )
    
    report_card = FileField('Fotocopy Rapor (PNG/JPG/JPEG/PDF)',
        validators=[
            FileRequired(message='File rapor harus diunggah'),
            FileAllowed(['png', 'jpg', 'jpeg', 'pdf'], 'Hanya file PNG, JPG, JPEG, atau PDF yang diizinkan')
        ]
    )
    
    non_athlete_statement = FileField('Pernyataan Bukan Atlet (PDF)',
        validators=[
            FileRequired(message='File pernyataan bukan atlet harus diunggah'),
            FileAllowed(['pdf'], 'Hanya file PDF yang diizinkan')
        ]
    )
    
    submit = SubmitField('Daftar', 
        render_kw={"class": "button button--primary"}
    )
    
    def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError('Email sudah terdaftar. Silakan gunakan email lain.')
            
    def validate_team_size(self, field):
        if field.data < 1:
            raise ValidationError('Jumlah anggota minimal 1 orang')