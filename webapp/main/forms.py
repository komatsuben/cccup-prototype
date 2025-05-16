from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional

class LoginForm(FlaskForm):
    username = StringField('Username atau Email', 
        validators=[
            DataRequired(message='Username atau email harus diisi'),
            Length(min=3, max=100, message='Panjang harus antara 3 sampai 100 karakter')
        ],
        render_kw={"placeholder": "Masukkan username atau email Anda"}
    )
    password = PasswordField('Kata Sandi',
        validators=[
            DataRequired(message='Kata sandi harus diisi'),
            Length(min=8, message='Kata sandi minimal 8 karakter')
        ],
        render_kw={"placeholder": "Masukkan kata sandi Anda", "id": "password"}
    )
    show_password = BooleanField('Tampilkan kata sandi', 
        id='show-password',
        render_kw={"onclick": "togglePassword()"}
    )
    submit = SubmitField('Masuk', 
        render_kw={"class": "button button--primary"}
    )