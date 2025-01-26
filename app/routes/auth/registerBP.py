# app/routes/auth/registerBP.py

# 📋 File defining the routes related to user registration.

from flask import current_app
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mail import Message
from app import mail, bcrypt
from validate_email_address import validate_email
from app.models import User, generate_unique_code
from datetime import datetime, timezone

# 🔷 1. Blueprint definition for handling user registration routes.
# The prefix `/register` is automatically added to all routes defined in this blueprint.
registerBp = Blueprint('register', __name__, url_prefix='/auth/register')

# 🔷 2. Main route for the registration page.
# This function handles both GET and POST requests.
@registerBp.route('/', methods=['GET', 'POST'])
def register_view():

    # 📩 When the form is submitted (POST method).
    if request.method == 'POST':
        # 🔹 Retrieve form data.
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        # 1️⃣ Validate that the required fields are not empty.
        if not username or not email or not password:
            flash('Fields marked with an asterisk are required.', 'danger')
            return redirect(url_for('register.register_view'))

        # 2️⃣ Check if the username or email are already registered.
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            if existing_user.username == username:
                flash('The username is already registered. Please choose another.', 'danger')
            if existing_user.email == email:
                flash('The email is already registered. Please log in or choose another.', 'danger')
            return redirect(url_for('register.register_view'))

        # 3️⃣ Validate the email format using the `validate_email` library.
        if not validate_email(email):
            flash('Please enter a valid email address.', 'danger')
            return redirect(url_for('register.register_view'))

        # 4️⃣ Validate password security.
        if not validate_password(password):
            flash('The password must have at least 8 characters, one uppercase letter, one number, and one special character.', 'danger')
            return redirect(url_for('register.register_view'))

        # 5️⃣ Generate a random 6-digit verification code.
        verification_code = generate_unique_code(User, 'verification_code', length=6)
        recovery_pin = generate_unique_code(User, 'recovery_pin', length=6)

        # 🕒 Set the current UTC timestamp for logging and tracking.
        timestamp = datetime.now(timezone.utc)

        # 6️⃣ Temporarily store user data in the session.
        session['pending_user'] = {
            'username': username,
            'email': email,
            'password_hash': bcrypt.generate_password_hash(password).decode('utf-8'),
            'verification_code': verification_code,
            'recovery_pin': recovery_pin,
            'timestamp': timestamp
        }

        # 🔹 Save the email in the session for use during verification.
        session['email_to_verify'] = email

        # 7️⃣ Attempt to send the verification email.
        try:
            send_verification_email(email, verification_code)
            flash('Registration initiated. Check your email to verify your account.', 'success')
            return redirect(url_for('verify.verify_view'))
        except Exception as e:
            # ❗ Catch errors when sending the email.
            flash(f'Error sending the verification email: {str(e)} \nCheck your email settings and internet connection.', 'danger')
            return redirect(url_for('register.register_view'))

    # 🖥️ For a GET request, render the registration page.
    return render_template('auth/register.html')

# 🔷 3. Function to send a verification email to the user.
def send_verification_email(email, code):
    """
    Sends an email containing the verification code to the user.
    """
    # 🕒 Set the current UTC timestamp.
    timestamp = datetime.now(timezone.utc)

    # 🔹 Save the code and timestamp in the session.
    pending_user = session.get('pending_user', {})
    pending_user['verification_code'] = code
    pending_user['timestamp'] = timestamp
    session['pending_user'] = pending_user

    # ✉️ Configure the email message.
    msg = Message(
        subject='Verify your account',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],  # Uses centralized configuration.
        recipients=[email]
    )
    # 🔹 Message body with the verification code.
    msg.html = render_template('auth/verification_email.html', code=code)

    # 📤 Send the email.
    mail.send(msg)

# 🔷 4. Function to validate password security.
def validate_password(password):
    """
    Validates that the password meets the following requirements:
    - At least 8 characters.
    - At least one uppercase letter.
    - At least one number.
    - At least one special character (e.g., @, $, !, %, *, ?, or &).
    """
    import re  # 📐 Use regular expressions to check the requirements.
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(pattern, password)


