# app/routes/auth/recovery_passBP.py

# 📦 IMPORTACIÓN DE MÓDULOS
from flask import Blueprint, render_template, request, flash, redirect, url_for
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import db, mail, bcrypt
from app.models import User
from app.routes.auth.registerBP import validate_password

# 🧩 Definir el Blueprint para la funcionalidad de recuperación de contraseña
recovery_passBp = Blueprint('recovery_pass', __name__)

# ➕ 1. RUTA PARA SOLICITAR RECUPERACIÓN DE CONTRASEÑA
serializer = URLSafeTimedSerializer('clave_secreta_super_segura')

# Ruta para solicitar recuperación de contraseña
@recovery_passBp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # Generar y enviar correo con token
            send_reset_email(user)
            flash('Se ha enviado un correo para restablecer tu contraseña.', 'info')
            return redirect(url_for('login.login_view'))
        else:
            flash('No se encontró una cuenta con ese correo.', 'danger')
    return render_template('auth/reset_password_request.html')

# 📧 FUNCIÓN PARA ENVIAR EL CORREO DE RECUPERACIÓN
def send_reset_email(user):
    token = serializer.dumps(user.email, salt='password-reset-salt')
    reset_url = url_for('recovery_pass.reset_password', token=token, _external=True)
    msg = Message(
        subject='Restablece tu contraseña',
        sender='noreply@tuapp.com',
        recipients=[user.email],
    )
    msg.body = f'''Para restablecer tu contraseña, visita el siguiente enlace:
               {reset_url}

                Si no solicitaste este cambio, ignora este mensaje.'''
    mail.send(msg)

# ✏️ 2. RUTA PARA RESTABLECER LA CONTRASEÑA
@recovery_passBp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        # Validar el token
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)  # Token válido por 1 hora
    except Exception:
        flash('El enlace de recuperación es inválido o ha expirado.', 'danger')
        return redirect(url_for('recovery_pass.reset_password_request'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('recovery_pass.reset_password_request'))

    if request.method == 'POST':
        new_password = request.form.get('password', '')
        if new_password:
            # 4️⃣ Validar la seguridad de la contraseña.
            if not validate_password(new_password):
                flash('La contraseña debe tener al menos 8 caracteres, una letra mayúscula, un número y un carácter especial.', 'danger')
                return redirect(url_for('recovery_pass.reset_password', token=token))

            # 🔐 Actualizar la contraseña en la base de datos
            user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
            db.session.commit()
            return render_template('auth/reset_password.html', success=True)

    return render_template('auth/reset_password.html')
