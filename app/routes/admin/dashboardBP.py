# app/routes/admin/dashboardBP.py

# 📦 MODULE IMPORTS
from flask import Blueprint, render_template, redirect, url_for, request, flash  # 🌐 Route handling, redirection, and flash messages
from flask_login import login_required, current_user  # 🔐 Authentication management
from app.models import User  # 👤 User model
from app import db  # 🗄️ Database
from sqlalchemy.exc import SQLAlchemyError, IntegrityError  # ❗ Database error handling
from functools import wraps  # 🧰 Tool for creating custom decorators

# 🧩 1. BLUEPRINT DEFINITION
# This blueprint groups all routes related to administration.
dashboardBp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# 🛡️ 2. `admin_required` DECORATOR
# This decorator ensures that only administrators can access protected routes.
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 🔒 Verify if the user is authenticated and an admin
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("You do not have permission to access this page.", "danger")  # ⚠️ Warning message
            return redirect(url_for('home.home'))  # 🔄 Redirect to home page
        return f(*args, **kwargs)
    return decorated_function

# 🖥️ 3. ADMIN DASHBOARD ROUTE (`/admin/dashboard`)
@dashboardBp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """
    Displays the admin panel with user search and pagination.
    """

    # 📝 Retrieve the search term from URL parameters
    search_query = request.args.get('search', '')

    # 🔎 Create the base query to search for users
    users_query = User.query
    if search_query:
        # 🔍 Filter by username or email matching the search term
        users_query = users_query.filter(
            (User.username.ilike(f"%{search_query}%")) | (User.email.ilike(f"%{search_query}%"))
        )

    # 📄 Pagination: Display 5 users per page
    page = request.args.get('page', 1, type=int)
    users = users_query.paginate(page=page, per_page=5)

    # 📊 Render the admin dashboard or results
    return render_template('admin/dashboard.html', users=users, search_query=search_query)

# ➕ 4. ROUTE TO ADD A NEW USER (`/admin/add_user`)
@dashboardBp.route('/add_user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    """
    Allows adding a new user to the system. Requires admin privileges.
    """
    # If the form method is 'POST'
    if request.method == 'POST':
        try:
            # 📥 Retrieve form data
            username = request.form.get('username').strip()
            email = request.form.get('email').strip()
            password = request.form.get('password').strip()
            is_admin = 'is_admin' in request.form  # ✅ Is admin?
            is_verified = 'is_verified' in request.form  # ✅ Is verified?

            # 🚨 Validate required fields
            if not username or not email or not password:
                flash('Fields with asterisks are required.', 'danger')
                return redirect(url_for('dashboard.add_user'))

            # 🆕 Create a new user
            new_user = User(username=username, email=email, is_admin=is_admin, is_verified=is_verified)
            new_user.set_password(password)  # 🔐 Set the password

            # 🗄️ Save the user to the database
            db.session.add(new_user)
            db.session.commit()
            flash('User successfully created.', 'success')

        except IntegrityError as e:
            db.session.rollback()
            if "username" in str(e.orig):
                flash('The username is already in use. Choose another.', 'danger')
            elif "email" in str(e.orig):
                flash('The email is already registered. Use a different one.', 'danger')
            else:
                flash('Data integrity error. Try again.', 'danger')
            return redirect(url_for('dashboard.add_user'))

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Error: {e} when updating the user. Try again.', 'danger')
            return redirect(url_for('dashboard.add_user'))

        return redirect(url_for('dashboard.dashboard'))

    return render_template('admin/add_user.html')

# ✏️ 5. ROUTE TO EDIT AN EXISTING USER (`/admin/edit_user/<user_id>`)
@dashboardBp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """
    Allows editing the details of an existing user.
    """
    # 🔍 Find the user or return a 404 if not found
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        try:
            # 📥 Retrieve form data
            username = request.form.get('username').strip()
            email = request.form.get('email').strip()
            user.is_admin = 'is_admin' in request.form
            user.is_verified = 'is_verified' in request.form

            # 🚨 Validate required fields
            if not username or not email:
                flash('Fields with asterisks are required.', 'danger')
                return redirect(url_for('dashboard.edit_user', user_id=user_id))

            # ✏️ Update user data
            user.username = username
            user.email = email
            new_password = request.form.get('password')
            if new_password:
                user.set_password(new_password)

            # 💾 Save changes
            db.session.commit()
            flash('User successfully updated.', 'success')

        except IntegrityError as e:
            db.session.rollback()
            if "username" in str(e.orig):
                flash('The username is already in use. Choose another.', 'danger')
            elif "email" in str(e.orig):
                flash('The email is already registered. Use a different one.', 'danger')
            else:
                flash('Data integrity error. Try again.', 'danger')
            return redirect(url_for('dashboard.edit_user', user_id=user_id))

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Error: {e} when updating the user. Try again.', 'danger')
            return redirect(url_for('dashboard.edit_user', user_id=user_id))

        return redirect(url_for('dashboard.dashboard'))

    return render_template('admin/edit_user.html', user=user)

# 🗑️ 6. ROUTE TO DELETE A USER (`/admin/delete_user/<user_id>`)
@dashboardBp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """
    Deletes a user from the system. Requires admin privileges.
    """
    try:
        # 🔍 Find the user or return a 404 if not found
        user = User.query.get_or_404(user_id)
        db.session.delete(user)  # ❌ Delete user
        db.session.commit()
        flash('User successfully deleted.', 'success')

    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error: {e} when deleting the user. Try again.', 'danger')

    return redirect(url_for('dashboard.dashboard'))

