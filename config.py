# config.py #


# 🧩 1. NECESSARY MODULE IMPORTS
import os  # 📂 Handling paths and environment variables
from dotenv import load_dotenv  # 🔐 Securely load variables from a .env file

# 🔐 2. Load environment variables from a `.env` file
load_dotenv()

# ⚙️ 3. MAIN CONFIGURATION CLASS
class Config:
    """Main configuration for the Flask application."""

    # 3.1 🔑 Secret key to protect sessions and forms
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not defined in the .env file")

    # 3.2 🗄️ PostgreSQL database connection URL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///default.db')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL is not defined in the .env file")

    # 3.3 ⚡ Disable modification tracking to improve performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 3.4 📧 Flask-Mail configuration for sending emails
    MAIL_SERVER = 'smtp.gmail.com'  # Gmail SMTP server
    MAIL_PORT = 587  # Secure port with TLS
    MAIL_USE_TLS = True  # Use of TLS (Transport Layer Security)
    MAIL_USERNAME = os.environ.get('EMAIL_USER')  # Username (email address)
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')  # Email password
    MAIL_DEFAULT_SENDER = os.getenv('SENDER', 'default_sender@example.com')  # Sender's address

    """
    This file configures and initializes all extensions, defines the factory function
    to create the Flask application, and registers blueprints. It also handles sessions
    and injects global data such as the current year.
    """


