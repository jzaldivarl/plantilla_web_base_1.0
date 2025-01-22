# app/routes/homeBP.py #

# Importamos los módulos necesarios desde Flask
from flask import Blueprint, render_template  # Blueprint para modularizar rutas, render_template para cargar templates

# Importamos login_required de Flask-Login para proteger rutas (aunque no se usa actualmente en este archivo)
from flask_login import login_required  # Requiere autenticación para acceder a ciertas vistas

# Definimos un blueprint para las rutas del home
home_bp = Blueprint('home', __name__, url_prefix='/home')

# Ruta principal del blueprint
@home_bp.route('/')
# @login_required  # Este decorador se puede usar si solo quieres permitir acceso a usuarios autenticados
def home():
    """
    Renderiza la página principal del sitio web (home).
    """
    return render_template('home.html')  # Carga y devuelve el archivo 'home.html'
