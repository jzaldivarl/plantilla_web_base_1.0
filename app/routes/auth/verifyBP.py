# app/routes/auth/verifyBP.py

# 📦 IMPORTACIÓN DE MÓDULOS
from flask import current_app
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mail import Message
from app import mail
from datetime import datetime, timezone, timedelta
from app import db  # 📚 Conexión a la base de datos
from app.models import User, generate_unique_code
from app.routes.auth.registerBP import send_verification_email  # 📧 Función para enviar emails de verificación
from functools import wraps  # 🛠️ Para crear decoradores personalizados
import random  # 🎲 Para generar códigos de verificación aleatorios

# 🔧 1. DEFINICIÓN DEL BLUEPRINT
# El Blueprint agrupa rutas relacionadas con la verificación.
verifyBp = Blueprint('verify', __name__, url_prefix='/verify')

# ⏰ 2. CONSTANTE DE TIEMPO DE VALIDEZ DEL CÓDIGO
# El código de verificación será válido por 5 minutos.
CODE_VALIDITY_PERIOD = timedelta(minutes=5)

# 🛡️ 3. DECORADOR `require_verification` (Protección de rutas)
# 🔒 Este decorador asegura que solo los usuarios en proceso de verificación puedan acceder a ciertas rutas.
def require_verification(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        pending_user = session.get('pending_user')  # 🔍 Busca el usuario pendiente en la sesión.

        # 🛑 Si no hay usuario pendiente o el email ya está registrado, se bloquea el acceso.
        if not pending_user or User.query.filter_by(email=pending_user['email']).first():
            flash('Acceso denegado. Ruta reservada solo para usuarios en proceso de verificación.', 'danger')
            return redirect(url_for('register.register_view'))

        # ✅ Si el usuario pendiente es válido, ejecuta la función original.
        return f(*args, **kwargs)
    return decorated_function

# 📄 4. RUTA `/verify/` — Página de verificación
# Muestra un formulario para que el usuario ingrese el código de verificación enviado por email.
@verifyBp.route('/', methods=['GET', 'POST'])
@require_verification  # 🛡️ Protege esta ruta usando el decorador `require_verification`.
def verify_view():
    if request.method == 'POST':  # 🖊️ Si el usuario envía el formulario...
        code = request.form.get('code', '').strip()  # 📥 Obtiene el código ingresado.

        pending_user = session.get('pending_user')  # 🔍 Busca el usuario pendiente en la sesión.

        # 🛑 Si no hay datos del usuario pendiente, redirige al registro.
        if not pending_user:
            flash('No se encontraron datos de registro. Por favor, regístrate nuevamente.', 'danger')
            return redirect(url_for('register.register_view'))

        # ⏳ Verifica si el código ha expirado.
        if 'timestamp' not in pending_user or datetime.now(timezone.utc) > pending_user['timestamp'] + CODE_VALIDITY_PERIOD:
            flash('El código de verificación ha expirado. Solicita uno nuevo.', 'danger')
            return redirect(url_for('verify.verify_view'))

        # 🔐 Verifica si el código ingresado coincide con el enviado por email.
        if pending_user['verification_code'] != code:
            # ⚠️ Incrementa los intentos fallidos.
            session['failed_attempts'] = session.get('failed_attempts', 0) + 1

            # 🚨 Si hay 3 o más intentos fallidos, limpia la sesión y redirige al registro.
            if session['failed_attempts'] >= 3:
                session.clear()
                flash('Has alcanzado el límite de intentos fallidos. Regístrate nuevamente.', 'danger')
                return redirect(url_for('register.register_view'))
            else:
                flash('Código incorrecto. Por favor, intenta nuevamente.', 'danger')
                return redirect(url_for('verify.verify_view'))

        # 🆕 Si el código es correcto, crea un nuevo usuario en la base de datos.
        new_user = User(
            username=pending_user['username'],
            email=pending_user['email'],
            password_hash=pending_user['password_hash'],
            recovery_pin=pending_user['recovery_pin'],  # Asegura que el PIN se guarda
            is_verified=True  # ✅ Marca al usuario como verificado.
        )
        db.session.add(new_user)  # 💾 Guarda el usuario en la base de datos.
        db.session.commit()  # 🔐 Confirma los cambios.

        # Enviar el correo con el PIN de recuperación al nuevo usuario
        send_pin_email(new_user)

        # 🧹 Limpia los datos relacionados con la verificación en la sesión.
        session.pop('pending_user', None)
        session.pop('email_to_verify', None)
        session.pop('failed_attempts', None)

        # 🎉 Muestra un mensaje de éxito y redirige al inicio de sesión.
        flash('Cuenta verificada y registrada exitosamente. Tu PIN de recuperación ha sido enviado a tu correo.\n'
                                   'Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login.login_view'))

    # 🖥️ Si el método es GET, muestra la página de verificación.
    return render_template('auth/verify.html')

# 🔄 5. RUTA `/verify/resend_code` — Reenvío del código de verificación
# Permite al usuario reenviar el código de verificación a su email.
@verifyBp.route('/resend_code', methods=['POST'])
@require_verification  # 🛡️ Protege esta ruta usando el decorador `require_verification`.
def resend_code():
    pending_user = session.get('pending_user')  # 🔍 Busca el usuario pendiente en la sesión.

    # 🛑 Si no se encuentra un usuario pendiente, devuelve un mensaje de error.
    if not pending_user or 'email' not in pending_user:
        return jsonify({'message': 'No se encontró la solicitud de verificación. Por favor, regístrate nuevamente.', 'category': 'danger', 'redirect': url_for('register.register_view')})

    # 📛 Limita los intentos de reenvío del código.
    attempts = session.get('resend_attempts', 0)
    if attempts >= 2:
        # 🛑 Si se alcanzó el límite, limpia la sesión y redirige al registro.
        session.clear()
        return jsonify({'message': 'Has alcanzado el número máximo de reenvíos. Redirigiendo al registro...', 'category': 'danger', 'redirect': url_for('register.register_view'), 'delay': 3000})

    # 🔄 Incrementa el contador de intentos de reenvío.
    session['resend_attempts'] = attempts + 1

    # 🔐 Mantiene el mismo código si aún es válido.
    if 'timestamp' in pending_user and datetime.now(timezone.utc) <= pending_user['timestamp'] + CODE_VALIDITY_PERIOD:
        new_code = pending_user['verification_code']
    else:
        # 🎲 Genera un nuevo código si el anterior ha expirado.
        #new_code = str(random.randint(100000, 999999))
        new_code = generate_unique_code(User, 'verification_code', length=6)
        pending_user['verification_code'] = new_code
        pending_user['timestamp'] = datetime.now(timezone.utc)
        session['pending_user'] = pending_user

    try:
        # 📧 Envía el código de verificación por email.
        send_verification_email(pending_user['email'], new_code)
        return jsonify({'message': 'El código de verificación ha sido reenviado. Revisa tu correo electrónico.', 'category': 'info'}), 200

    except Exception as e:
        # ❌ Si ocurre un error, devuelve un mensaje de error.
        return jsonify({'message': f'Error al enviar el correo: {str(e)}', 'category': 'danger'}), 500


def send_pin_email(user):
    """
    Envía un correo electrónico al usuario con el PIN de recuperación.
    """
    msg = Message(
        subject="Bienvenido a la Aplicación - Código PIN de Recuperación",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email]
    )
    msg.body = f"""
    Hola {user.username},

    Gracias por registrarte en nuestra aplicación.

    Aquí tienes tu código PIN de recuperación:
    {user.recovery_pin}

    Es importante que guardes este código en un lugar seguro.
    Lo necesitarás si alguna vez olvidas tu contraseña.

    ¡Bienvenido y esperamos que disfrutes de nuestra plataforma!

    Saludos,
    El equipo de soporte
    """
    mail.send(msg)


