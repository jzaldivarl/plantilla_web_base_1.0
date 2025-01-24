# config.py #


# 🧩 1. IMPORTACIÓN DE MÓDULOS NECESARIOS
import os  # 📂 Manejo de rutas y variables de entorno
from dotenv import load_dotenv  # 🔐 Carga segura de variables desde un archivo .env

# 🔐 2. Cargar las variables de entorno desde un archivo `.env`
load_dotenv()

# ⚙️ 3. CLASE DE CONFIGURACIÓN PRINCIPAL
class Config:
    """Configuración principal de la aplicación Flask."""

    # 3.1 🔑 Llave secreta para proteger sesiones y formularios
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY no está definida en el archivo .env")

    # 3.2 🗄️ URL de conexión a la base de datos PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///default.db')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL no está definida en el archivo .env")

    # 3.3 ⚡ Desactiva el rastreo de modificaciones para mejorar el rendimiento
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 3.4 📧 Configuración de Flask-Mail para el envío de correos electrónicos
    MAIL_SERVER = 'smtp.gmail.com'  # Servidor SMTP de Gmail
    MAIL_PORT = 587  # Puerto seguro con TLS
    MAIL_USE_TLS = True  # Uso de TLS (Transport Layer Security)
    MAIL_USERNAME = os.environ.get('EMAIL_USER')  # Usuario (correo electrónico)
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')  # Contraseña del correo
    MAIL_DEFAULT_SENDER = os.getenv('SENDER', 'default_sender@example.com')  # Dirección del remitente


    """
    Este archivo configura e inicializa todas las extensiones, define la función de fábrica
    para crear la aplicación Flask y registra blueprints, además de manejar sesiones y la
    inyección de datos globales como el año actual.

    """

