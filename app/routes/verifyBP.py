# app/routes/verifyBP.py #

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app import db
from app.models import User
import random
from app.routes.registerBP import send_verification_email # ✅ Importa la función correctamente
from functools import wraps


# Definición del Blueprint para la ruta de verificación
verifyBp = Blueprint('verify', __name__, url_prefix='/verify')

# Decorador para proteger la ruta /verify
def require_verification(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        pending_user = session.get('pending_user')
        # Si no hay usuario pendiente o si el usuario está verificado, redirigir al registro
        if not pending_user or User.query.filter_by(email=pending_user['email']).first():
            flash('Acceso denegado. Ruta reservada solo para reenvío de código.', 'danger')
            return redirect(url_for('register.register_view'))
        return f(*args, **kwargs)
    return decorated_function

# Ruta para la página de verificación
@verifyBp.route('/', methods=['GET', 'POST'])
@require_verification
def verify_view():

    if request.method == 'POST':

        # # Obtiene el código ingresado por el usuario
        code = request.form.get('code', '').strip()

        # capturar usuario pendiente de verificación en la sesión
        pending_user = session.get('pending_user')

        # verificar si existe el usuario
        if not pending_user:
            # mensaje para el usuario
            flash('No se encontraron datos de registro. Por favor, regístrate nuevamente.', 'danger')
            return redirect(url_for('register.register_view'))

        # Verificar si el código ingresado coincide con el código generado
        if pending_user['verification_code'] != code:
            # mensaje para el usuario
            flash('Código incorrecto. Por favor, intenta de nuevo.', 'danger')
            return redirect(url_for('verify.verify_view'))

        # Crear un nuevo usuario y guardarlo en la base de datos
        new_user = User(
            username=pending_user['username'],
            email=pending_user['email'],
            password_hash=pending_user['password_hash'],
            is_verified= True
        )
        db.session.add(new_user)
        db.session.commit()

        # Limpiar la sesión
        session.pop('pending_user', None)
        session.pop('email_to_verify', None)

        # mensaje para el usuario
        flash('Cuenta verificada y registrada exitosamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login.login_view'))

    return render_template('verify.html')

# Ruta para reenviar el código de verificación
@verifyBp.route('/resend_code', methods=['POST'])
def resend_code():

    # capturar el valor del usuario en la sesion temporal
    pending_user = session.get('pending_user')

    # verificar si existe el usuario y su correo)
    if not pending_user or 'email' not in pending_user:
        return jsonify({'status': 'error', 'message': 'No se encontró la solicitud de verificación.'}), 400

    # Limitar los intentos de reenvío
    attempts = session.get('resend_attempts', 0)
    if attempts >= 3:
        # Limpiar la sesión y redirigir al registro
        session.clear()
        return jsonify({
            'status': 'error',
            'message': 'Has alcanzado el límite de reenvíos. Por favor, regístrate nuevamente.',
            'redirect': url_for('register.register_view')
        }), 429

    # Incrementar el contador de intentos
    session['resend_attempts'] = attempts + 1

    # Extraer el email del usuario pendiente
    email = pending_user['email']
    # Generar un nuevo código de verificación
    new_code = str(random.randint(100000, 999999))
    pending_user['verification_code'] = new_code
    session['pending_user'] = pending_user  # Actualizar la sesión

    # Enviar el nuevo código de verificación por correo electrónico
    try:
        send_verification_email(email, new_code)
        return jsonify({'status': 'success', 'message': 'El código de verificación ha sido reenviado.'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error al enviar el correo: {str(e)}'}), 500
