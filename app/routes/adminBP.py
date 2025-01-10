# app/routes/adminBP.py #

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import User
from app import db
from functools import wraps


# Definir el blueprint
adminBp = Blueprint('admin', __name__, url_prefix='/admin')

# Decorador para verificar si el usuario es administrador
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("No tienes permisos para acceder a esta página.", "danger")
            return redirect(url_for('home.home'))  # Cambia 'home.home' si es necesario
        return f(*args, **kwargs)
    return decorated_function

# 🖥️ Ruta del Dashboard de Administración
@adminBp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    users = User.query.all()
    return render_template('admin/dashboard.html', users=users)


# ➕ Ruta para agregar un nuevo usuario
@adminBp.route('/add_user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        is_admin = 'is_admin' in request.form
        is_verified = 'is_verified' in request.form

        # Validar que los campos no estén vacíos
        if not username or not email or not password:
            flash('Los campos con asteriscos son obligatorios.', 'danger')
            return redirect(url_for('admin.add_user'))

        # Crear y guardar el nuevo usuario
        new_user = User(
            username=username,
            email=email,
            is_admin=is_admin,
            is_verified=is_verified
        )
        new_user.set_password(password)
        # adicionar y salvar los nuevos datos en la BD
        db.session.add(new_user)
        db.session.commit()

        flash('Usuario creado exitosamente.', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/add_user.html')


# ✏️ Ruta para editar un usuario existente
@adminBp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        user.is_admin = 'is_admin' in request.form
        user.is_verified = 'is_verified' in request.form

        # Validar que los campos no estén vacíos
        if not username or not email:
            flash('Los campos con asteriscos son obligatorios.', 'danger')
            return redirect(url_for('admin.edit_user', user_id=user_id))

        # Actualizar los datos del usuario
        user.username = username
        user.email = email

        # Manejar los checkboxes correctamente
        user.is_admin = 'is_admin' in request.form
        user.is_verified = 'is_verified' in request.form

        # Cambiar contraseña solo si el campo no está vacío
        new_password = request.form.get('password')
        if new_password:
            user.set_password(new_password)

        # Guardar cambios en la base de datos
        db.session.commit()

        flash('Usuario actualizado exitosamente.', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/edit_user.html', user=user)

# 🗑️ Ruta para eliminar un usuario
@adminBp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    flash('Usuario eliminado exitosamente.', 'success')
    return redirect(url_for('admin.dashboard'))
