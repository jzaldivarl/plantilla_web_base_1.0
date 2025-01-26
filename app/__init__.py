# app/__init__.py - Configuration and Initialization of the Flask Application


"""
This file configures and initializes all extensions, defines the factory function 
to create the Flask application, and registers blueprints. It also handles sessions 
and injects global data such as the current year.

Returns: app
"""

# 🧩 1. IMPORT REQUIRED MODULES
from flask import Flask  # 🌐 Flask for web application creation
from flask_sqlalchemy import SQLAlchemy  # 🗄️ Database management
from flask_bcrypt import Bcrypt  # 🔐 Secure password hashing
from flask_login import LoginManager  # 👤 User session management
from flask_migrate import Migrate  # 🏗️ Database migrations
from flask_mail import Mail  # 📧 Email sending
from config import Config  # ⚙️ Application configuration
from datetime import datetime  # 🕒 Injecting the current year into templates
from flask_wtf.csrf import CSRFProtect  # 🛡️ CSRF attack protection

# 🔧 2. GLOBAL INITIALIZATION OF EXTENSIONS
db = SQLAlchemy()  # Database initialization
bcrypt = Bcrypt()  # Password hashing
login_manager = LoginManager()  # User session management
mail = Mail()  # Email handling
migrate = Migrate()  # Migrations for updating the database
csrf = CSRFProtect()  # CSRF attack protection

# 🚀 3. FACTORY FUNCTION TO CREATE THE FLASK APPLICATION
def create_app():
    """Creates and configures the main Flask application instance."""
    app = Flask(__name__)

    # 3.1 📋 Load configuration from `config.py`
    app.config.from_object(Config)

    # 3.2 🔧 Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # 3.3 🏷️ Configure the default login route
    login_manager.login_view = 'login.login_view'

    # 3.4 🧩 Import and register models
    from app.models import User

    # 3.5 🧩 Import and register blueprints
    from app.routes.auth.loginBP import loginBp
    from app.routes.auth.registerBP import registerBp
    from app.routes.auth.verifyBP import verifyBp
    from app.routes.auth.recovery_passBP import recovery_passBp
    from app.routes.admin.dashboardBP import dashboardBp
    from app.routes.homeBP import homeBp
    from app.routes.errorsBP import errorsBp

    # 3.6 📂 Register blueprints in the application
    app.register_blueprint(loginBp)
    app.register_blueprint(registerBp)
    app.register_blueprint(verifyBp)
    app.register_blueprint(recovery_passBp)
    app.register_blueprint(dashboardBp)
    app.register_blueprint(homeBp)
    app.register_blueprint(errorsBp)

    # 3.7 👤 Load the current user from the session
    @login_manager.user_loader
    def load_user(user_id):
        """Loads a user from the database by their ID."""
        return User.query.get(int(user_id))

    # 3.8 🗓️ Inject the current year into all templates
    @app.context_processor
    def inject_year():
        """Adds the current year to all templates."""
        return {'current_year': datetime.now().year}

    return app


