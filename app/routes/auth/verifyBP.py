# app/routes/auth/verifyBP.py

# 📦 MODULE IMPORTS
from flask import current_app
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mail import Message
from app import mail
from datetime import datetime, timezone, timedelta
from app import db  # 📚 Database connection
from app.models import User, generate_unique_code
<<<<<<< HEAD
from app.routes.auth.registerBP import send_verification_email  # 📧 Función para enviar emails de verificación
from functools import wraps  # 🛠️ Para crear decoradores personalizados
=======
from app.routes.auth.registerBP import send_verification_email  # 📧 Function to send verification emails
from functools import wraps  # 🛠️ To create custom decorators
import random  # 🎲 To generate random verification codes
>>>>>>> f159f3042523ac0d81801038b491a0268a052302

# 🔧 1. BLUEPRINT DEFINITION
# The Blueprint groups routes related to verification.
verifyBp = Blueprint('verify', __name__, url_prefix='/verify')

# ⏰ 2. CODE VALIDITY PERIOD CONSTANT
# The verification code will be valid for 5 minutes.
CODE_VALIDITY_PERIOD = timedelta(minutes=5)

# 🛡️ 3. `require_verification` DECORATOR (Route Protection)
# 🔒 This decorator ensures that only users in the verification process can access certain routes.
def require_verification(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        pending_user = session.get('pending_user')  # 🔍 Searches for the pending user in the session.

        # 🛑 If there is no pending user or the email is already registered, access is blocked.
        if not pending_user or User.query.filter_by(email=pending_user['email']).first():
            flash('Access denied. Route reserved for users in the verification process only.', 'danger')
            return redirect(url_for('register.register_view'))

        # ✅ If the pending user is valid, the original function is executed.
        return f(*args, **kwargs)
    return decorated_function

# 📄 4. `/verify/` ROUTE — Verification Page
# Displays a form for the user to enter the verification code sent by email.
@verifyBp.route('/', methods=['GET', 'POST'])
@require_verification  # 🛡️ Protects this route using the `require_verification` decorator.
def verify_view():
    if request.method == 'POST':  # 🖊️ If the user submits the form...
        code = request.form.get('code', '').strip()  # 📥 Gets the entered code.

        pending_user = session.get('pending_user')  # 🔍 Searches for the pending user in the session.

        # 🛑 If no pending user data is found, redirects to the registration page.
        if not pending_user:
            flash('No registration data found. Please register again.', 'danger')
            return redirect(url_for('register.register_view'))

        # ⏳ Checks if the code has expired.
        if 'timestamp' not in pending_user or datetime.now(timezone.utc) > pending_user['timestamp'] + CODE_VALIDITY_PERIOD:
            flash('The verification code has expired. Please request a new one.', 'danger')
            return redirect(url_for('verify.verify_view'))

        # 🔐 Verifies if the entered code matches the one sent by email.
        if pending_user['verification_code'] != code:
            # ⚠️ Increments failed attempts.
            session['failed_attempts'] = session.get('failed_attempts', 0) + 1

            # 🚨 If there are 3 or more failed attempts, clears the session and redirects to the registration page.
            if session['failed_attempts'] >= 3:
                session.clear()
                flash('You have reached the maximum number of failed attempts. Please register again.', 'danger')
                return redirect(url_for('register.register_view'))
            else:
                flash('Incorrect code. Please try again.', 'danger')
                return redirect(url_for('verify.verify_view'))

        # 🆕 If the code is correct, creates a new user in the database.
        new_user = User(
            username=pending_user['username'],
            email=pending_user['email'],
            password_hash=pending_user['password_hash'],
            recovery_pin=pending_user['recovery_pin'],  # Ensures the PIN is saved
            is_verified=True  # ✅ Marks the user as verified.
        )
        db.session.add(new_user)  # 💾 Saves the user in the database.
        db.session.commit()  # 🔐 Confirms the changes.

        # Sends the recovery PIN email to the new user
        send_pin_email(new_user)

        # 🧹 Cleans up verification-related data from the session.
        session.pop('pending_user', None)
        session.pop('email_to_verify', None)
        session.pop('failed_attempts', None)

        # 🎉 Displays a success message and redirects to the login page.
        flash('Account successfully verified and registered. Your recovery PIN has been sent to your email.\n'
                                   'You can now log in.', 'success')
        return redirect(url_for('login.login_view'))

    # 🖥️ If the method is GET, displays the verification page.
    return render_template('auth/verify.html')

# 🔄 5. `/verify/resend_code` ROUTE — Resend Verification Code
# Allows the user to resend the verification code to their email.
@verifyBp.route('/resend_code', methods=['POST'])
@require_verification  # 🛡️ Protects this route using the `require_verification` decorator.
def resend_code():
    pending_user = session.get('pending_user')  # 🔍 Searches for the pending user in the session.

    # 🛑 If no pending user is found, returns an error message.
    if not pending_user or 'email' not in pending_user:
        return jsonify({'message': 'Verification request not found. Please register again.', 'category': 'danger', 'redirect': url_for('register.register_view')})

    # 📛 Limits the resend attempts.
    attempts = session.get('resend_attempts', 0)
    if attempts >= 2:
        # 🛑 If the limit is reached, clears the session and redirects to the registration page.
        session.clear()
        return jsonify({'message': 'You have reached the maximum number of resends. Redirecting to registration...', 'category': 'danger', 'redirect': url_for('register.register_view'), 'delay': 3000})

    # 🔄 Increments the resend attempts counter.
    session['resend_attempts'] = attempts + 1

    # 🔐 Keeps the same code if it is still valid.
    if 'timestamp' in pending_user and datetime.now(timezone.utc) <= pending_user['timestamp'] + CODE_VALIDITY_PERIOD:
        new_code = pending_user['verification_code']
    else:
        # 🎲 Generates a new code if the previous one has expired.
        #new_code = str(random.randint(100000, 999999))
        new_code = generate_unique_code(User, 'verification_code', length=6)
        pending_user['verification_code'] = new_code
        pending_user['timestamp'] = datetime.now(timezone.utc)
        session['pending_user'] = pending_user

    try:
        # 📧 Sends the verification code by email.
        send_verification_email(pending_user['email'], new_code)
        return jsonify({'message': 'The verification code has been resent. Please check your email.', 'category': 'info'}), 200

    except Exception as e:
        # ❌ If an error occurs, returns an error message.
        return jsonify({'message': f'Error sending email: {str(e)}', 'category': 'danger'}), 500


def send_pin_email(user):
    """
    Sends an email to the user with the recovery PIN.
    """
    msg = Message(
        subject="Welcome to the Application - Recovery PIN Code",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email]
    )
    msg.body = f"""
    Hello {user.username},

    Thank you for registering in our application.

    Here is your recovery PIN code:
    {user.recovery_pin}

    It is important to store this code in a safe place.
    You will need it if you ever forget your password.

    Welcome, and we hope you enjoy our platform!

    Regards,
    The support team
    """
    mail.send(msg)


