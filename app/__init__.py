# app/__init__.py - Configuración e inicialización de la aplicación Flask

# 🧩 IMPORTACIÓN DE MÓDULOS NECESARIOS
from flask import Flask  # 🌐 Flask para la creación de la aplicación web
from flask_sqlalchemy import SQLAlchemy  # 🗄️ Manejo de base de datos
from flask_bcrypt import Bcrypt  # 🔐 Hashing seguro de contraseñas
from flask_login import LoginManager  # 👤 Gestión de sesiones de usuario
from flask_migrate import Migrate  # 🏗️ Migraciones de la base de datos
from flask_mail import Mail  # 📧 Envío de correos electrónicos
from config import Config  # ⚙️ Configuración de la aplicación
from datetime import datetime  # 🕒 Inyección del año actual en las plantillas
from flask_wtf.csrf import CSRFProtect  # 🛡️ Protección contra ataques CSRF


# 🔧 INICIALIZACIÓN GLOBAL DE EXTENSIONES
db = SQLAlchemy()  # Inicialización de la base de datos
bcrypt = Bcrypt()  # Hashing de contraseñas
login_manager = LoginManager()  # Manejo de sesiones de usuario
mail = Mail()  # Manejo de correos electrónicos
migrate = Migrate()  # Migraciones para actualizar la base de datos
csrf = CSRFProtect()  # Protección contra ataques CSRF

# 🚀 FUNCIÓN DE FÁBRICA PARA CREAR LA APLICACIÓN FLASK
def create_app():
    """Crea y configura la instancia principal de la aplicación Flask."""
    app = Flask(__name__)

    # 📋 Cargar la configuración desde `config.py`
    app.config.from_object(Config)

    # 🔧 Inicializar las extensiones
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # 🏷️ Configurar la ruta de inicio de sesión por defecto
    login_manager.login_view = 'login.login_view'

    # 🧩 Importar y registrar los modelos
    from app.models import User

    # 🧩 Importar y registrar los blueprints
    from app.routes.auth.loginBP import loginBp
    from app.routes.auth.registerBP import registerBp
    from app.routes.auth.verifyBP import verifyBp
    from app.routes.auth.recovery_passBP import recovery_passBp
    from app.routes.admin.dashboardBP import dashboardBp
    from app.routes.homeBP import homeBp
    from app.routes.errorsBP import errorsBp


    # 📂 Registrar los blueprints en la aplicación
    app.register_blueprint(loginBp)
    app.register_blueprint(registerBp)
    app.register_blueprint(verifyBp)
    app.register_blueprint(recovery_passBp)
    app.register_blueprint(dashboardBp)
    app.register_blueprint(homeBp)
    app.register_blueprint(errorsBp)


    # 👤 Cargar el usuario actual desde la sesión
    @login_manager.user_loader
    def load_user(user_id):
        """Carga un usuario desde la base de datos por su ID."""
        return User.query.get(int(user_id))

    # 🗓️ Inyectar el año actual en todas las plantillas
    @app.context_processor
    def inject_year():
        """Añade el año actual a todas las plantillas."""
        return {'current_year': datetime.now().year}

    return app


