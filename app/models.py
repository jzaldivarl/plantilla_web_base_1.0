# app/models.py #

from app import db, bcrypt
from flask_login import UserMixin
import random
import string

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6), nullable=False, default=lambda: str(random.randint(100000, 999999)))
    is_verified = db.Column(db.Boolean, default=False)

    # Método para establecer el hash de la contraseña
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Método para verificar la contraseña
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_verification_code():
        return ''.join(random.choices(string.digits, k=6))
