# app/models.py - Definición de modelos para la base de datos

from app import db, bcrypt  # Importa la base de datos y la utilidad de hashing de contraseñas
from flask_login import UserMixin  # Importa UserMixin para gestionar sesiones de usuario
import random  # Utilizado para generar códigos de verificación
import string  # Proporciona caracteres para la generación de códigos aleatorios

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
        default=lambda: str(random.randint(100000, 999999))
    )  # Código de verificación por defecto
    is_verified = db.Column(db.Boolean, default=False)  # Indica si el usuario ha verificado su cuenta

    # Método para establecer el hash de la contraseña
    def set_password(self, password):
        """
        Genera y almacena el hash de la contraseña del usuario.
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Método para verificar la contraseña
    def check_password(self, password):
        """
        Verifica si la contraseña proporcionada coincide con el hash almacenado.
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_verification_code():
        """
        Genera un código de verificación de 6 dígitos.
        """
        return ''.join(random.choices(string.digits, k=6))
