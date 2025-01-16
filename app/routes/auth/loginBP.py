# app/routes/auth/loginBP.py

# 📦 IMPORTACIÓN DE MÓDULOS
from flask import Blueprint, render_template, request, redirect, url_for, flash  # 🌐 Módulos para rutas y manejo de mensajes flash
from flask_login import login_user, logout_user, login_required  # 🔐 Manejo de sesiones de usuario
from app.models import User  # 👤 Modelo de usuario para consultas en la base de datos

# 🧩 1. CREAR EL BLUEPRINT
# 🔖 El blueprint agrupa las rutas relacionadas con el inicio de sesión y el cierre de sesión.
loginBp = Blueprint('login', __name__, url_prefix='/auth/login')

# 🔑 2. RUTA DE INICIO DE SESIÓN (`/auth/login`)
# Esta ruta permite a los usuarios iniciar sesión en la aplicación.
@loginBp.route('/', methods=['GET', 'POST'])
def login_view():

    # 🖊️ Si el usuario envía el formulario (método POST) ...
    if request.method == 'POST':
        # 📥 Obtener los datos del formulario
        email = request.form.get('email').strip()  # ✉️ Email ingresado por el usuario
        password = request.form.get('password').strip()  # 🔒 Contraseña ingresada por el usuario

        # 🚨 2. Validación básica de formato de correo (en backend)
        if not email or '@' not in email:
            flash('Correo inválido. Por favor, ingresa un correo válido.', 'danger')
            return redirect(url_for('login.login_view'))

        # 🔎 3. BUSCAR USUARIO EN LA BASE DE DATOS
        # Filtra el usuario por el email ingresado.
        user = User.query.filter_by(email=email).first()

        # ✅ 4. VERIFICACIÓN DE CREDENCIALES
        # Si el usuario existe y la contraseña es correcta...
        if user and user.check_password(password):
            # 🚫 5. BLOQUEAR ACCESO SI NO ESTÁ VERIFICADO (excepto si es admin)
            if not user.is_admin and not user.is_verified:
                flash('Tu cuenta no está verificada. Por favor, verifica tu email.', 'warning')
                return redirect(url_for('login.login_view'))  # 🔄 Redirige al formulario de inicio de sesión

            # 🔓 6. INICIAR SESIÓN
            # Si todo está correcto, iniciar sesión con Flask-Login.
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')  # 🎉 Mensaje de éxito

            # 🔀 7. REDIRIGIR SEGÚN EL TIPO DE USUARIO
            # Si es administrador, redirige al panel de administración.
            if user.is_admin:
                return redirect(url_for('dashboard.dashboard'))
            else:
                # Si es un usuario normal, redirige a la página de inicio.
                return redirect(url_for('home.home'))

        else:
            # ⚠️ 8. CREDENCIALES INCORRECTAS
            # Si las credenciales no son correctas, muestra un mensaje de error.
            flash('Credenciales incorrectas. Por favor, intenta nuevamente.', 'danger')

    # 🖥️ Renderiza el formulario de inicio de sesión (método GET).
    return render_template('auth/login.html')

# 🚪 9. RUTA PARA CERRAR SESIÓN (`/login/logout`)
# Esta ruta permite a los usuarios cerrar sesión.
@loginBp.route('/logout')
@login_required  # 🔒 Requiere que el usuario esté autenticado.
def logout():
    # 🚪 10. CERRAR SESIÓN
    # Cierra la sesión del usuario actual.
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')  # 💬 Mensaje de información
    # 🔄 Redirige al formulario de inicio de sesión.
    return redirect(url_for('login.login_view'))

