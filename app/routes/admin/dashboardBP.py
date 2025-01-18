# app/routes/admin/dashboardBP.py

# 📦 IMPORTACIÓN DE MÓDULOS
from flask import Blueprint, render_template, redirect, url_for, request, flash  # 🌐 Manejo de rutas, redirección y mensajes flash
from flask_login import login_required, current_user  # 🔐 Manejo de autenticación
from app.models import User  # 👤 Modelo de usuario
from app import db  # 🗄️ Base de datos
from validate_email_address import validate_email  # 📧 Validación de correos electrónicos
from app.routes.auth.registerBP import validate_password  # 🔒 Validación de contraseñas
from sqlalchemy.exc import SQLAlchemyError, IntegrityError  # ❗ Manejo de errores de la base de datos
from functools import wraps  # 🧰 Herramienta para crear decoradores personalizados

# 🧩 1. DEFINICIÓN DEL BLUEPRINT
# Este blueprint agrupa todas las rutas relacionadas con la administración.
dashboardBp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# 🛡️ 2. DECORADOR `admin_required`
# Este decorador asegura que solo los administradores puedan acceder a las rutas protegidas.
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 🔒 Verifica si el usuario está autenticado y es administrador
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("No tienes permisos para acceder a esta página.", "danger")  # ⚠️ Mensaje de advertencia
            return redirect(url_for('home.home'))  # 🔄 Redirección a la página de inicio
        return f(*args, **kwargs)
    return decorated_function

# 🖥️ 3. RUTA DEL DASHBOARD DE ADMINISTRACIÓN (`/admin/dashboard`)
@dashboardBp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # 📝 Obtener el término de búsqueda de los parámetros de la URL
    search_query = request.args.get('search', '')

    # 🔎 Crear la consulta base para los usuarios
    users_query = User.query
    if search_query:
        # 🔍 Filtrar por nombre de usuario o email que coincida con el término de búsqueda
        users_query = users_query.filter(
            (User.username.ilike(f"%{search_query}%")) | (User.email.ilike(f"%{search_query}%"))
        )

    # 📄 Paginación: Mostrar 5 usuarios por página
    page = request.args.get('page', 1, type=int)
    users = users_query.paginate(page=page, per_page=5)

    # 📊 Renderizar el dashboard de administración
    return render_template('admin/dashboard.html', users=users, search_query=search_query)

# ➕ 4. RUTA PARA AGREGAR UN NUEVO USUARIO (`/admin/add_user`)
@dashboardBp.route('/add_user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        try:
            # 📥 Obtener los datos del formulario
            username = request.form.get('username').strip()
            email = request.form.get('email').strip()
            password = request.form.get('password').strip()
            is_admin = 'is_admin' in request.form  # ✅ ¿Es administrador?
            is_verified = 'is_verified' in request.form  # ✅ ¿Está verificado?

            # 🚨 Validación de campos obligatorios
            if not username or not email or not password:
                flash('Los campos con asteriscos son obligatorios.', 'danger')
                return redirect(url_for('dashboard.add_user'))

            # 🆕 Crear un nuevo usuario
            new_user = User(username=username, email=email, is_admin=is_admin, is_verified=is_verified)
            new_user.set_password(password)  # 🔐 Establecer la contraseña

            # 🗄️ Guardar el usuario en la base de datos
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario creado exitosamente.', 'success')

        except IntegrityError as e:
            db.session.rollback()
            if "username" in str(e.orig):
                flash('El nombre de usuario ya está en uso. Elige otro.', 'danger')
            elif "email" in str(e.orig):
                flash('El correo electrónico ya está registrado. Usa uno diferente.', 'danger')
            else:
                flash('Error de integridad de datos. Intenta nuevamente.', 'danger')
            return redirect(url_for('dashboard.add_user'))

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Error: {e} al actualizar el usuario. Intenta nuevamente.', 'danger')
            return redirect(url_for('dashboard.add_user'))

        return redirect(url_for('dashboard.dashboard'))

    return render_template('admin/add_user.html')

# ✏️ 5. RUTA PARA EDITAR UN USUARIO EXISTENTE (`/admin/edit_user/<user_id>`)
@dashboardBp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)  # 🔍 Buscar usuario por ID
    if request.method == 'POST':
        try:
            # 📥 Obtener datos del formulario
            username = request.form.get('username').strip()
            email = request.form.get('email').strip()
            user.is_admin = 'is_admin' in request.form
            user.is_verified = 'is_verified' in request.form

            # 🚨 Validar campos obligatorios
            if not username or not email:
                flash('Los campos con asteriscos son obligatorios.', 'danger')
                return redirect(url_for('dashboard.edit_user', user_id=user_id))

            # ✏️ Actualizar datos del usuario
            user.username = username
            user.email = email
            new_password = request.form.get('password')
            if new_password:
                user.set_password(new_password)

            # 💾 Guardar cambios
            db.session.commit()
            flash('Usuario actualizado exitosamente.', 'success')

        except IntegrityError as e:
            db.session.rollback()
            if "username" in str(e.orig):
                flash('El nombre de usuario ya está en uso. Elige otro.', 'danger')
            elif "email" in str(e.orig):
                flash('El correo electrónico ya está registrado. Usa uno diferente.', 'danger')
            else:
                flash('Error de integridad de datos. Intenta nuevamente.', 'danger')
            return redirect(url_for('dashboard.edit_user', user_id=user_id))

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Error: {e} al actualizar el usuario. Intenta nuevamente.', 'danger')
            return redirect(url_for('dashboard.edit_user', user_id=user_id))

        return redirect(url_for('dashboard.dashboard'))

    return render_template('admin/edit_user.html', user=user)

# 🗑️ 6. RUTA PARA ELIMINAR UN USUARIO (`/admin/delete_user/<user_id>`)
@dashboardBp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)  # 🔍 Buscar usuario por ID
        db.session.delete(user)  # ❌ Eliminar usuario
        db.session.commit()
        flash('Usuario eliminado exitosamente.', 'success')

    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error: {e} al eliminar el usuario. Intenta nuevamente.', 'danger')

    return redirect(url_for('dashboard.dashboard'))


