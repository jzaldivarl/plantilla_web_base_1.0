from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models import User

# Crear blueprint
loginBp = Blueprint('login', __name__, url_prefix='/login')

# Rutas de login
@loginBp.route('/', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':

        email = request.form.get('email').strip()  # Obtenemos el email del formulario
        password = request.form.get('password').strip()

        # Busca al usuario por su email
        user = User.query.filter_by(email=email).first()

        # Verificar credenciales
        if user and user.check_password(password):
            # los usuarios que no son administradores
            # y tampoco están verificados se bloquean aquí
            if not user.is_admin and not user.is_verified:
                flash('Tu cuenta no está verificada. Por favor, verifica tu email.', 'warning')
                return redirect(url_for('login.login_view'))

            # Si pasa la verificación o es admin, iniciar sesión
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('home.home'))
        else:
            flash('Credenciales incorrectas.', 'danger')
            return redirect(url_for('login.login_view'))

    return render_template('login.html')



# Ruta de logout
@loginBp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('login.login_view'))
