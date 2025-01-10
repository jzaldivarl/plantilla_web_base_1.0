# app/routes/registerBP.py #

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mail import Message
from app import mail, bcrypt
from validate_email_address import validate_email
import random

# Definición del Blueprint para la ruta de registro
registerBp = Blueprint('register', __name__, url_prefix='/register')

# Ruta para la página de registro
@registerBp.route('/', methods=['GET', 'POST'])
def register_view():

    if request.method == 'POST':
        # Obtener y validar datos del formulario
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        # 1️⃣ Validar que los campos no estén vacíos
        if not username or not email or not password:
            flash('Los campos con asteriscos son obligatorios.', 'danger')
            return redirect(url_for('register.register_view'))

        # 2️⃣ Validar que el nombre de usuario tenga al menos 5 caracteres
        if len(username) < 5:
            flash('El nombre de usuario debe tener al menos 5 caracteres.', 'danger')
            return redirect(url_for('register.register_view'))

        # 3️⃣ Validar formato del email usando validate_email
        if not validate_email(email):
            flash('Por favor, ingresa un correo electrónico válido.', 'danger')
            return redirect(url_for('register.register_view'))

        # 4️⃣ Validar que la contraseña tenga al menos 8 caracteres, una mayúscula y un carácter especial
        if not validate_password(password):
            flash('La contraseña debe tener al menos 8 caracteres, una letra mayúscula, un número y un carácter especial.', 'danger')
            return redirect(url_for('register.register_view'))

        # 5️⃣ Generar un código de verificación (Código de 6 dígitos)
        verification_code = str(random.randint(100000, 999999))

        # 6️⃣ Almacenar los datos en la sesión temporalmente hasta que el usuario verifique su email
        session['pending_user'] = {
            'username': username,
            'email': email,
            'password_hash': bcrypt.generate_password_hash(password).decode('utf-8'),
            'verification_code': verification_code
        }

        # Almacenar email en la sesión después de todas las validaciones
        session['email_to_verify'] = email

        # 7️⃣ Enviar el correo de verificación
        try:
            send_verification_email(email, verification_code)
            flash('Registro iniciado. Revisa tu correo para verificar tu cuenta.', 'success')
            return redirect(url_for('verify.verify_view'))
        except Exception as e:
            flash(f'Error al enviar el correo de verificación: {str(e)}', 'danger')
            return redirect(url_for('register.register_view'))

    return render_template('register.html')

# Función para enviar el correo con el código de verificación
def send_verification_email(email, code):
    msg = Message(
        subject='Verifica tu cuenta',
        sender='tu_correo@gmail.com',  # Reemplaza con tu dirección de correo
        recipients=[email]
    )
    msg.body = f'Tu código de verificación es: {code}'
    mail.send(msg)

# Función para validar la seguridad de la contraseña
def validate_password(password):
    import re
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(pattern, password)
