# app/routes/verifyBP.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User
import random
from app.routes.registerBP import send_verification_email  # ✅ Función de envío de correo
from functools import wraps

# Definición del Blueprint para la ruta de verificación
verifyBp = Blueprint('verify', __name__, url_prefix='/verify')

# ✅ Decorador para proteger la ruta /verify
def require_verification(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        pending_user = session.get('pending_user')
        # Si no hay usuario pendiente o si el usuario ya está verificado, redirigir al registro
        if not pending_user or User.query.filter_by(email=pending_user['email']).first():
            flash('Acceso denegado. Ruta reservada solo para usuarios en proceso de verificación.', 'danger')
            return redirect(url_for('register.register_view'))
        return f(*args, **kwargs)
    return decorated_function

# ✅ Ruta para la página de verificación
@verifyBp.route('/', methods=['GET', 'POST'])
@require_verification
def verify_view():
    if request.method == 'POST':
        code = request.form.get('code', '').strip()  # ✅ Obtiene el código ingresado
        pending_user = session.get('pending_user')  # ✅ Captura el usuario pendiente

        if not pending_user:
            flash('No se encontraron datos de registro. Por favor, regístrate nuevamente.', 'danger')
            return redirect(url_for('register.register_view'))

        # ✅ Verificar si el código ingresado coincide
        if pending_user['verification_code'] != code:
            flash('Código incorrecto. Por favor, intenta nuevamente.', 'danger')
            return redirect(url_for('verify.verify_view'))

        # ✅ Crear el nuevo usuario y guardar en la base de datos
        new_user = User(
            username=pending_user['username'],
            email=pending_user['email'],
            password_hash=pending_user['password_hash'],
            is_verified=True
        )
        db.session.add(new_user)
        db.session.commit()

        # ✅ Limpiar la sesión
        session.pop('pending_user', None)
        session.pop('email_to_verify', None)

        flash('Cuenta verificada y registrada exitosamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login.login_view'))

    return render_template('verify.html')

# ✅ Ruta para reenviar el código de verificación
@verifyBp.route('/resend_code', methods=['GET'])
@require_verification
def resend_code():
    pending_user = session.get('pending_user')

    if not pending_user or 'email' not in pending_user:
        flash('No se encontró la solicitud de verificación. Por favor, regístrate nuevamente.', 'danger')
        return redirect(url_for('register.register_view'))

    # ✅ Limitar los intentos de reenvío
    attempts = session.get('resend_attempts', 0)
    if attempts >= 3:
        session.clear()
        flash('Has alcanzado el límite de reenvíos. Por favor, regístrate nuevamente.', 'danger')
        return redirect(url_for('register.register_view'))

    # ✅ Incrementar los intentos
    session['resend_attempts'] = attempts + 1

    # ✅ Generar un nuevo código de verificación
    new_code = str(random.randint(100000, 999999))
    pending_user['verification_code'] = new_code
    session['pending_user'] = pending_user  # ✅ Actualizar la sesión

    try:
        send_verification_email(pending_user['email'], new_code)
        flash('El código de verificación ha sido reenviado. Revisa tu correo electrónico.', 'info')
    except Exception as e:
        flash(f'Error al enviar el correo: {str(e)}', 'danger')

    return redirect(url_for('verify.verify_view'))
