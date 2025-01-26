# app/routes/auth/loginBP.py


# 📦 MODULE IMPORTS
from flask import Blueprint, render_template, request, redirect, url_for, flash  # 🌐 Modules for routing and flash messages
from flask_login import login_user, logout_user, login_required  # 🔐 Session management for users
from app.models import User  # 👤 User model for database queries

# 🧩 1. CREATE THE BLUEPRINT
# 🔖 The blueprint groups routes related to login and logout functionality.
loginBp = Blueprint('login', __name__, url_prefix='/auth/login')

# 🔑 2. LOGIN ROUTE (`/auth/login`)
# This route allows users to log in to the application.
@loginBp.route('/', methods=['GET', 'POST'])
def login_view():

    # 🖊️ If the user submits the form (POST method)...
    if request.method == 'POST':
        # 📥 Retrieve form data
        email = request.form.get('email').strip()  # ✉️ Email entered by the user
        password = request.form.get('password').strip()  # 🔒 Password entered by the user

        # 🚨 2. Basic email format validation (backend)
        if not email or '@' not in email:
            flash('Invalid email. Please enter a valid email address.', 'danger')
            return redirect(url_for('login.login_view'))

        # 🔎 3. SEARCH FOR USER IN THE DATABASE
        # Filter the user by the entered email.
        user = User.query.filter_by(email=email).first()

        # ✅ 4. CREDENTIAL VERIFICATION
        # If the user exists and the password is correct...
        if user and user.check_password(password):
            # 🚫 5. BLOCK ACCESS IF NOT VERIFIED (except for admin users)
            if not user.is_admin and not user.is_verified:
                flash('Your account is not verified. Please verify your email.', 'warning')
                return redirect(url_for('login.login_view'))  # 🔄 Redirect to the login form

            # 🔓 6. LOG IN
            # If everything is correct, log in with Flask-Login.
            login_user(user)
            flash('Login successful.', 'success')  # 🎉 Success message

            # 🔀 7. REDIRECT BASED ON USER TYPE
            # If the user is an admin, redirect to the admin dashboard.
            if user.is_admin:
                return redirect(url_for('dashboard.dashboard'))
            else:
                # If the user is a regular user, redirect to the homepage.
                return redirect(url_for('home.home'))

        else:
            # ⚠️ 8. INCORRECT CREDENTIALS
            # If the credentials are incorrect, display an error message.
            flash('Invalid credentials. Please try again.', 'danger')

    # 🖥️ Render the login form (GET method).
    return render_template('auth/login.html')

# 🚪 9. LOGOUT ROUTE (`/login/logout`)
# This route allows users to log out.
@loginBp.route('/logout')
@login_required  # 🔒 Requires the user to be authenticated.
def logout():
    # 🚪 10. LOG OUT
    # Logs out the current user.
    logout_user()
    flash('You have successfully logged out.', 'info')  # 💬 Information message
    # 🔄 Redirect to the login form.
    return redirect(url_for('login.login_view'))

