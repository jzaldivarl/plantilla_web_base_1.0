# app/routes/auth/recovery_passBP.py

# 📦 MODULE IMPORTS
import os
from dotenv import load_dotenv  # To load variables from the .env file
from flask import current_app
from flask import Blueprint, render_template, request, flash, redirect, url_for
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import db, mail, bcrypt
from app.models import User, PasswordRecoveryAttempt
from app.routes.auth.registerBP import validate_password
from datetime import datetime, timezone, timedelta

# Load environment variables from the .env file
load_dotenv()

# 🧩 Define the Blueprint for password recovery functionality
# Create a Blueprint called "recovery_pass" to handle password recovery routes.
recovery_passBp = Blueprint('recovery_pass', __name__, url_prefix='/auth/recovery_pass')

# ➕ 1. ROUTE FOR REQUESTING PASSWORD RECOVERY
# URLSafeTimedSerializer instance to generate and verify secure tokens.
# The secret key ensures tokens are unique to this application.
serializer = URLSafeTimedSerializer(os.getenv('TOKEN_SECRET_KEY'))  # Key from .env

# Function to check password recovery attempt limits
def has_exceeded_recovery_limit(user):
    """Checks if the user has exceeded the recovery attempt limit in the last 3 hours."""
    limit = 3  # Allowed attempt limit per user
    time_window = datetime.now(timezone.utc) - timedelta(hours=3)  # Adjusted time window
    attempts = PasswordRecoveryAttempt.query.filter(
        PasswordRecoveryAttempt.user_id == user.id,
        PasswordRecoveryAttempt.timestamp >= time_window
    ).count()
    return attempts >= limit

def log_recovery_attempt(user):
    """Logs a password recovery attempt for a user."""
    attempt = PasswordRecoveryAttempt(user_id=user.id, timestamp=datetime.now(timezone.utc))
    db.session.add(attempt)
    db.session.commit()

# ➕ 1. ROUTE FOR REQUESTING PASSWORD RECOVERY
@recovery_passBp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """
    Route to handle password recovery requests.
    Now requires a PIN to validate the legitimacy of the request.
    """
    # If the request method is POST (form submitted)
    if request.method == 'POST':
        # Get the email and pin entered by the user in the form
        email = request.form.get('email')
        pin = request.form.get('pin')

        # Search for the user in the database by their email
        user = User.query.filter_by(email=email).first()

        # If the user exists
        if user:
            if has_exceeded_recovery_limit(user):
                flash('You have exceeded the attempt limit. Try again in 3 hours.', 'danger')
                return redirect(url_for('recovery_pass.reset_password_request'))

            # Validate that the entered PIN matches the user's PIN
            if user.recovery_pin == pin:
                # If the PIN is correct, send the recovery email
                send_reset_email(user)
                log_recovery_attempt(user)
                flash('A password reset email has been sent.', 'info')
                # Redirect to the login page after sending the email
                return redirect(url_for('login.login_view'))
            else:
                log_recovery_attempt(user)
                # If the PIN does not match, show an error message
                flash('The entered PIN is incorrect.', 'danger')
        else:
            # If the user does not exist, show an error message
            flash('No account found with that email.', 'danger')

    # Render the password recovery request template
    return render_template('auth/reset_password_request.html')

# 📧 FUNCTION TO SEND RECOVERY EMAIL
def send_reset_email(user):
    # Generate a unique token using the user's email and a specific salt
    token = serializer.dumps(user.email, salt='password-reset-salt')
    # Build the password reset URL with the generated token
    reset_url = url_for('recovery_pass.reset_password', token=token, _external=True)
    # Create the email message
    msg = Message(
        subject='Reset Your Password',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],  # Use centralized configuration.
        recipients=[user.email],    # Recipient address
    )
    # Message body with the reset URL
    msg.body = f'''To reset your password, visit the following link:
    {reset_url}

    If you did not request this change, please ignore this message.'''
    # Send the message via the configured mail server
    mail.send(msg)

# ✏️ 2. ROUTE TO RESET THE PASSWORD
@recovery_passBp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        # Validate the token using the salt and ensuring it has not expired (1-hour validity)
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except Exception:
        # If the token is invalid or has expired, show an error message
        flash('The recovery link is invalid or has expired.', 'danger')
        # Redirect to the page to request recovery again
        return redirect(url_for('recovery_pass.reset_password_request'))

    # Search for the user in the database using the email decoded from the token
    user = User.query.filter_by(email=email).first()
    if not user:
        # If the user is not found, show an error message
        flash('User not found.', 'danger')
        # Redirect to the page to request recovery again
        return redirect(url_for('recovery_pass.reset_password_request'))

    # If the request method is POST (form submitted)
    if request.method == 'POST':
        # Get the new password entered by the user
        new_password = request.form.get('password', '').strip()
        if new_password:
            # 4️⃣ Validate the password's security using the validation function
            if not validate_password(new_password):
                # If the password is invalid, show an error message
                flash('The password must be at least 8 characters long, include an uppercase letter, a number, and a special character.', 'danger')
                # Redirect to the current form with the token
                return redirect(url_for('recovery_pass.reset_password', token=token))

            # 🔐 If the password is valid, hash it
            user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
            # Save the changes to the database
            db.session.commit()
            # Render the template with a visual success confirmation
            return render_template('auth/reset_password.html', success=True)

    # Render the form to reset the password
    return render_template('auth/reset_password.html')


