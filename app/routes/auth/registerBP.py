# app/routes/auth/registerBP.py

# 📋 Archivo que define las rutas relacionadas con el registro de usuarios.

import random
from flask import current_app
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mail import Message
from app import mail, bcrypt
from validate_email_address import validate_email
from app.models import User, generate_unique_code
from datetime import datetime, timezone


# 🔷 1. Definición del Blueprint para manejar las rutas del registro de usuarios.
# El prefijo `/register` se agrega automáticamente a todas las rutas definidas en este blueprint.
registerBp = Blueprint('register', __name__, url_prefix='/auth/register')

# 🔷 2. Ruta principal para la página de registro.
# Esta función maneja tanto solicitudes GET como POST.
@registerBp.route('/', methods=['GET', 'POST'])
def register_view():

    # 📩 Cuando se envía el formulario (método POST).
    if request.method == 'POST':
        # 🔹 Obtener los datos del formulario.
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        # 1️⃣ Validar que los campos requeridos no estén vacíos.
        if not username or not email or not password:
            flash('Los campos con asteriscos son obligatorios.', 'danger')
            return redirect(url_for('register.register_view'))

        # 2️⃣ Verificar si el nombre de usuario o el correo ya están registrados.
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            if existing_user.username == username:
                flash('El nombre de usuario ya está registrado. Por favor, elige otro.', 'danger')
            if existing_user.email == email:
                flash('El correo electrónico ya está registrado. Por favor, inicia sesión o elige otro.', 'danger')
            return redirect(url_for('register.register_view'))

        # 3️⃣ Validar formato del email usando la librería `validate_email`.
        if not validate_email(email):
            flash('Por favor, ingresa un correo electrónico válido.', 'danger')
            return redirect(url_for('register.register_view'))

        # 4️⃣ Validar la seguridad de la contraseña.
        if not validate_password(password):
            flash('La contraseña debe tener al menos 8 caracteres, una letra mayúscula, un número y un carácter especial.', 'danger')
            return redirect(url_for('register.register_view'))

        # 5️⃣ Generar un código de verificación de 6 dígitos aleatorio.
        verification_code = generate_unique_code(User, 'verification_code', length=6)
        recovery_pin = generate_unique_code(User, 'recovery_pin', length=6)

        # 🕒 Establecer el timestamp actual en UTC para registro y seguimiento.
        timestamp = datetime.now(timezone.utc)

        # 6️⃣ Almacenar los datos del usuario en la sesión de forma temporal.
        session['pending_user'] = {
            'username': username,
            'email': email,
            'password_hash': bcrypt.generate_password_hash(password).decode('utf-8'),
            'verification_code': verification_code,
            'recovery_pin': recovery_pin,
            'timestamp': timestamp
        }

        # 🔹 Guardar el email en la sesión para usarlo en la verificación.
        session['email_to_verify'] = email

        # 7️⃣ Intentar enviar el correo de verificación.
        try:
            send_verification_email(email, verification_code)
            flash('Registro iniciado. Revisa tu correo para verificar tu cuenta.', 'success')
            return redirect(url_for('verify.verify_view'))
        except Exception as e:
            # ❗ Capturar errores al enviar el correo.
            flash(f'Error al enviar el correo de verificación: {str(e)} \n verifique su configuración de correo y su conexión de internet', 'danger')
            return redirect(url_for('register.register_view'))

    # 🖥️ Si es una solicitud GET, renderizar la página de registro.
    return render_template('auth/register.html')

# 🔷 3. Función para enviar el correo de verificación al usuario.
def send_verification_email(email, code):
    """
    Envía un correo electrónico con el código de verificación al usuario.
    """
    # 🕒 Establecer el timestamp actual en UTC.
    timestamp = datetime.now(timezone.utc)

    # 🔹 Guardar el código y el timestamp en la sesión.
    pending_user = session.get('pending_user', {})
    pending_user['verification_code'] = code
    pending_user['timestamp'] = timestamp
    session['pending_user'] = pending_user

    # ✉️ Configurar el mensaje de correo.
    msg = Message(
        subject='Verifica tu cuenta',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],  # Usa la configuración centralizada.
        recipients=[email]
    )
    # 🔹 Cuerpo del mensaje con el código de verificación.
    msg.html = render_template('auth/verification_email.html', code=code)

    # 📤 Enviar el correo.
    mail.send(msg)

# 🔷 4. Función para validar la seguridad de la contraseña.
def validate_password(password):
    """
    Valida que la contraseña cumpla con los siguientes requisitos:
    - Al menos 8 caracteres.
    - Al menos una letra mayúscula.
    - Al menos un número.
    - Al menos un carácter especial (como @, $, !, %, *, ? o &).
    """
    import re  # 📐 Usar expresiones regulares para verificar los requisitos.
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(pattern, password)


