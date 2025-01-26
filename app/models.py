# app/models.py - Database Models Definition


"""
Overview:
This file contains the definition of the database models for the Flask application.

Defined models:
1. User:
   - Represents the application's users.
   - Includes basic information such as username, email, password, admin role, etc.
   - Methods:
     - `set_password`: Generates and stores the password hash.
     - `check_password`: Verifies a password against the stored hash.
     - `generate_verification_code`: Generates a unique 6-digit verification code.

2. PasswordRecoveryAttempt:
   - Logs users' password recovery attempts.
   - Methods:
     - `count_attempts_in_last_hour`: Counts recovery attempts in the last hour for a user.
     - `register_attempt`: Logs a new password recovery attempt.

3. Function `generate_unique_code`:
   - Generates a unique code that does not exist in the database for a specific model and column.
"""

from app import db, bcrypt  # Database and password hashing utility
from flask_login import UserMixin  # User session management
import random  # To generate verification codes
import string  # Provides characters for generating random codes
from datetime import datetime, timezone, timedelta  # Time and date management

# User model
class User(UserMixin, db.Model):
    """
    Model representing a user in the database.
    Includes basic information, credentials, and user roles.
    """
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    username = db.Column(db.String(80), nullable=False, unique=True)  # Unique username
    email = db.Column(db.String(120), nullable=False, unique=True)  # Unique email
    password_hash = db.Column(db.String(128), nullable=False)  # Password hash
    is_admin = db.Column(db.Boolean, default=False)  # Indicates if the user is an admin
    verification_code = db.Column(
        db.String(6),
        nullable=False,
        default=lambda: str(random.randint(100000, 999999))  # Default verification code
    )
    is_verified = db.Column(db.Boolean, default=False)  # Indicates if the user has verified their account
    recovery_pin = db.Column(
        db.String(6),
        nullable=False,
        unique=True,
        default=lambda: generate_unique_code(User, 'recovery_pin'))
    # Generates a unique 6-digit PIN associated with the user for recovery.

    # Relationship with password recovery attempts
    recovery_attempts = db.relationship(
        'PasswordRecoveryAttempt', backref='user', lazy=True, cascade="all, delete-orphan"
    )

    # Method to set the password hash
    def set_password(self, password):
        """Generates and stores the user's password hash."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Method to verify the password
    def check_password(self, password):
        """Verifies if the provided password matches the stored hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_verification_code():
        """Generates a 6-digit verification code."""
        return ''.join(random.choices(string.digits, k=6))


# Model for managing password recovery attempts
class PasswordRecoveryAttempt(db.Model):
    """
    Model logging each user's password recovery attempts.
    """
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each record
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Related user's ID
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))  # Attempt's timestamp

    @staticmethod
    def count_attempts_in_last_hour(user_id):
        """
        Counts password recovery attempts in the last hour for a specific user.
        """
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        return PasswordRecoveryAttempt.query.filter(
            PasswordRecoveryAttempt.user_id == user_id,
            PasswordRecoveryAttempt.timestamp >= one_hour_ago
        ).count()

    @staticmethod
    def register_attempt(user_id):
        """
        Logs a new password recovery attempt for a user.
        """
        attempt = PasswordRecoveryAttempt(user_id=user_id)
        db.session.add(attempt)
        db.session.commit()


def generate_unique_code(model, column_name, length=6):
    """
    Generates a unique code that does not exist in the specified model's column.

    Args:
        model (db.Model): The model to check for collisions.
        column_name (str): The column name to verify uniqueness.
        length (int): The length of the generated code (default is 6).

    Returns:
        str: A unique code.
    """
    while True:
        code = f"{random.randint(10**(length-1), 10**length - 1)}"
        # Check if the code already exists in the database
        exists = db.session.query(model.query.filter(getattr(model, column_name) == code).exists()).scalar()
        if not exists:
            return code


