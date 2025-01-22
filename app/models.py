# app/models.py - Definición de modelos para la base de datos

"""
Resumen:
Este archivo contiene la definición de los modelos de la base de datos para la aplicación Flask.

Modelos definidos:
1. User:
   - Representa a los usuarios de la aplicación.
   - Incluye información básica como nombre de usuario, correo electrónico, contraseña, rol de administrador, etc.
   - Métodos:
     - `set_password`: Genera y almacena el hash de la contraseña.
     - `check_password`: Verifica una contraseña con el hash almacenado.
     - `generate_verification_code`: Genera un código de verificación único de 6 dígitos.

2. PasswordRecoveryAttempt:
   - Registra intentos de recuperación de contraseñas de los usuarios.
   - Métodos:
     - `count_attempts_in_last_hour`: Cuenta los intentos de recuperación en la última hora para un usuario.
     - `register_attempt`: Registra un nuevo intento de recuperación de contraseña.

3. Función `generate_unique_code`:
   - Genera un código único no existente en la base de datos para un modelo y columna específicos.
"""

from app import db, bcrypt  # Base de datos y utilidad de hashing de contraseñas
from flask_login import UserMixin  # Gestión de sesiones de usuario
import random  # Para generar códigos de verificación
import string  # Proporciona caracteres para la generación de códigos aleatorios
from datetime import datetime, timezone, timedelta  # Manejo de fechas y tiempos

# Modelo de usuario
class User(UserMixin, db.Model):
    """
    Modelo que representa a un usuario en la base de datos.
    Incluye información básica, credenciales y roles de usuario.
    """
    id = db.Column(db.Integer, primary_key=True)  # ID único para cada usuario
    username = db.Column(db.String(80), nullable=False, unique=True)  # Nombre de usuario único
    email = db.Column(db.String(120), nullable=False, unique=True)  # Correo electrónico único
    password_hash = db.Column(db.String(128), nullable=False)  # Hash de la contraseña
    is_admin = db.Column(db.Boolean, default=False)  # Indica si el usuario es administrador
    verification_code = db.Column(
        db.String(6),
        nullable=False,
        default=lambda: str(random.randint(100000, 999999))  # Código de verificación por defecto
    )
    is_verified = db.Column(db.Boolean, default=False)  # Indica si el usuario ha verificado su cuenta
    recovery_pin = db.Column(db.String(6), nullable=False, unique=True, default=lambda: generate_unique_code(User, 'recovery_pin'))
    # Se genera un PIN único de 6 dígitos asociado al usuario para recuperación.

    # Relación con intentos de recuperación de contraseña
    recovery_attempts = db.relationship(
        'PasswordRecoveryAttempt', backref='user', lazy=True, cascade="all, delete-orphan"
    )

    # Método para establecer el hash de la contraseña
    def set_password(self, password):
        """Genera y almacena el hash de la contraseña del usuario."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Método para verificar la contraseña
    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con el hash almacenado."""
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_verification_code():
        """Genera un código de verificación de 6 dígitos."""
        return ''.join(random.choices(string.digits, k=6))


# Modelo para gestionar intentos de recuperación de contraseña
class PasswordRecoveryAttempt(db.Model):
    """
    Modelo que registra cada intento de recuperación de contraseña de los usuarios.
    """
    id = db.Column(db.Integer, primary_key=True)  # ID único para cada registro
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ID del usuario relacionado
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))  # Fecha y hora del intento

    @staticmethod
    def count_attempts_in_last_hour(user_id):
        """
        Cuenta los intentos de recuperación en la última hora para un usuario específico.
        """
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        return PasswordRecoveryAttempt.query.filter(
            PasswordRecoveryAttempt.user_id == user_id,
            PasswordRecoveryAttempt.timestamp >= one_hour_ago
        ).count()

    @staticmethod
    def register_attempt(user_id):
        """
        Registra un nuevo intento de recuperación de contraseña para un usuario.
        """
        attempt = PasswordRecoveryAttempt(user_id=user_id)
        db.session.add(attempt)
        db.session.commit()


def generate_unique_code(model, column_name, length=6):
    """
    Genera un código único que no existe en la columna especificada de un modelo.

    Args:
        model (db.Model): El modelo en el que buscar colisiones.
        column_name (str): El nombre de la columna donde verificar unicidad.
        length (int): La longitud del código generado (por defecto 6).

    Returns:
        str: Un código único.
    """
    while True:
        code = f"{random.randint(10**(length-1), 10**length - 1)}"
        # Verifica si el código ya existe en la base de datos
        exists = db.session.query(model.query.filter(getattr(model, column_name) == code).exists()).scalar()
        if not exists:
            return code
