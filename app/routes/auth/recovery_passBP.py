# app/routes/auth/recovery_passBP.py

# 📦 IMPORTACIÓN DE MÓDULOS
import os
from dotenv import load_dotenv  # Para cargar las variables desde el archivo .env
from flask import current_app
from flask import Blueprint, render_template, request, flash, redirect, url_for
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import db, mail, bcrypt
from app.models import User
from app.routes.auth.registerBP import validate_password

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# 🧩 Definir el Blueprint para la funcionalidad de recuperación de contraseña
# Se crea un Blueprint llamado "recovery_pass" para manejar rutas relacionadas con la recuperación de contraseñas.
recovery_passBp = Blueprint('recovery_pass', __name__, url_prefix='/auth/recovery_pass')

def get_serializer():
    return URLSafeTimedSerializer(current_app.config['TOKEN_SECRET_KEY'])

# ➕ 1. RUTA PARA SOLICITAR RECUPERACIÓN DE CONTRASEÑA
# Instancia de URLSafeTimedSerializer para generar y verificar tokens seguros.
# La clave secreta asegura que los tokens sean únicos para esta aplicación.
serializer = URLSafeTimedSerializer(os.getenv('TOKEN_SECRET_KEY')) # Clave desde .env


# Ruta para solicitar recuperación de contraseña
@recovery_passBp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    # Si el método de la solicitud es POST (formulario enviado)
    if request.method == 'POST':
        # Obtener el correo electrónico ingresado por el usuario
        email = request.form.get('email')
        # Buscar al usuario en la base de datos usando el correo electrónico
        user = User.query.filter_by(email=email).first()
        if user:
            # Si el usuario existe, enviar un correo electrónico de recuperación
            send_reset_email(user)
            flash('Se ha enviado un correo para restablecer tu contraseña.', 'info')
            # Redirigir al inicio de sesión después de enviar el correo
            return redirect(url_for('login.login_view'))
        else:
            # Si el usuario no existe, mostrar un mensaje de error
            flash('No se encontró una cuenta con ese correo.', 'danger')
    # Renderizar la plantilla para solicitar recuperación de contraseña
    return render_template('auth/reset_password_request.html')

# 📧 FUNCIÓN PARA ENVIAR EL CORREO DE RECUPERACIÓN
def send_reset_email(user):
    # Generar un token único utilizando el correo del usuario y un salt específico
    token = serializer.dumps(user.email, salt='password-reset-salt')
    # Construir la URL de restablecimiento de contraseña con el token generado
    reset_url = url_for('recovery_pass.reset_password', token=token, _external=True)
    # Crear el mensaje de correo
    msg = Message(
        subject='Restablece tu contraseña',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],  # Usa la configuración centralizada.
        recipients=[user.email],    # Dirección del destinatario
    )
    # Cuerpo del mensaje con la URL de restablecimiento
    msg.body = f'''Para restablecer tu contraseña, visita el siguiente enlace:
    {reset_url}

    Si no solicitaste este cambio, ignora este mensaje.'''
    # Enviar el mensaje a través del servidor de correo configurado
    mail.send(msg)

# ✏️ 2. RUTA PARA RESTABLECER LA CONTRASEÑA
@recovery_passBp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        # Validar el token utilizando el salt y asegurando que no haya expirado (1 hora de validez)
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except Exception:
        # Si el token es inválido o ha expirado, mostrar un mensaje de error
        flash('El enlace de recuperación es inválido o ha expirado.', 'danger')
        # Redirigir a la página para solicitar nuevamente la recuperación
        return redirect(url_for('recovery_pass.reset_password_request'))

    # Buscar al usuario en la base de datos utilizando el correo decodificado del token
    user = User.query.filter_by(email=email).first()
    if not user:
        # Si no se encuentra al usuario, mostrar un mensaje de error
        flash('Usuario no encontrado.', 'danger')
        # Redirigir a la página para solicitar nuevamente la recuperación
        return redirect(url_for('recovery_pass.reset_password_request'))

    # Si el método de la solicitud es POST (formulario enviado)
    if request.method == 'POST':
        # Obtener la nueva contraseña ingresada por el usuario
        new_password = request.form.get('password', '')
        if new_password:
            # 4️⃣ Validar la seguridad de la contraseña utilizando la función de validación
            if not validate_password(new_password):
                # Si la contraseña no es válida, mostrar un mensaje de error
                flash('La contraseña debe tener al menos 8 caracteres, una letra mayúscula, un número y un carácter especial.', 'danger')
                # Redirigir al formulario actual con el token
                return redirect(url_for('recovery_pass.reset_password', token=token))

            # 🔐 Si la contraseña es válida, generar un hash de la misma
            user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
            # Guardar los cambios en la base de datos
            db.session.commit()
            # Renderizar la plantilla con una confirmación visual de éxito
            return render_template('auth/reset_password.html', success=True)

    # Renderizar el formulario para restablecer la contraseña
    return render_template('auth/reset_password.html')

