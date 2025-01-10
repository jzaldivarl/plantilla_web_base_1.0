# app/__init__.py #

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config
from datetime import datetime
from flask_wtf.csrf import CSRFProtect


# Inicializar extensiones
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configuración de Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'jorge83py@gmail.com'
    app.config['MAIL_PASSWORD'] = 'gobskgncvpnpxcdv'

    # Inicializar extensiones con la app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app) # ✅ Aplica CSRF a toda la app
    login_manager.login_view = 'login.login_view'

    # Importar modelos
    from app.models import User

    # Importar blueprints
    from app.routes.loginBP import loginBp
    from app.routes.registerBP import registerBp
    from app.routes.verifyBP import verifyBp
    from app.routes.adminBP import adminBp
    from app.routes.homeBP import homeBp
    from app.routes.errorsBP import errorsBp

    # Importar blueprints
    app.register_blueprint(loginBp)
    app.register_blueprint(registerBp)
    app.register_blueprint(verifyBp)
    app.register_blueprint(adminBp)
    app.register_blueprint(homeBp)
    app.register_blueprint(errorsBp)

    # Cargar usuario desde la sesión
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Añade un contexto para el año actual
    @app.context_processor
    def inject_year():
        return {'current_year': datetime.now().year}


    return app
