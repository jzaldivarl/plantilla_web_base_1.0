# app/routes/errorsBP.py

# 📋 Archivo de rutas para la gestión de errores en la aplicación Flask.

from flask import Blueprint, render_template, redirect, url_for, flash, current_app

# 🧩 Crea un blueprint llamado 'errors' que agrupa los manejadores de errores.
# Esto permite organizar los controladores de errores en un módulo separado.
errorsBp = Blueprint('errors', __name__)

# ✅ Función común para manejar errores y redirigir al login.
# Esta función centraliza la lógica de redirección para errores comunes.
def handle_common_errors(error, message, category):
    """
    Muestra un mensaje de flash con la categoría especificada y redirige a la vista de login.

    - error: Objeto de error capturado.
    - message: Mensaje que se mostrará al usuario.
    - category: Categoría del mensaje (info, warning, danger).
    """
    flash(message, category)  # Muestra un mensaje flash al usuario.
    return redirect(url_for('loginBP.login_view'))  # Redirige al login.

# ⚠️ Manejo de errores específicos con sus respectivas funciones de controlador.

# 🛑 Error 401: No autorizado.
@errorsBp.app_errorhandler(401)
def unauthorized_error(error):
    """
    Manejador de errores para el código 401 (No autorizado).
    Se ejecuta cuando un usuario intenta acceder a una ruta protegida sin estar autenticado.
    """
    return handle_common_errors(error, 'No autorizado. Por favor, inicia sesión.', 'warning')

# 🛡️ Error 400: Solicitud incorrecta (por ejemplo, fallo de CSRF).
@errorsBp.app_errorhandler(400)
def handle_bad_request(error):
    """
    Manejador de errores para el código 400 (Solicitud incorrecta).
    Se ejecuta cuando Flask detecta un error relacionado con la seguridad,
    como un token CSRF faltante o inválido.
    """
    flash('Error de seguridad: token CSRF faltante o inválido.')  # Mensaje flash de error.
    return render_template('errors/400.html'), 400  # Renderiza la plantilla de error 400.

# 🚫 Error 403: Acceso denegado.
@errorsBp.app_errorhandler(403)
def forbidden_error(error):
    """
    Manejador de errores para el código 403 (Acceso denegado).
    Se ejecuta cuando un usuario intenta acceder a una ruta para la cual no tiene permisos.
    """
    return handle_common_errors(error, 'Acceso denegado. No tienes los permisos necesarios.', 'danger')

# 🔍 Error 404: Página no encontrada.
@errorsBp.app_errorhandler(404)
def not_found_error(error):
    """
    Manejador de errores para el código 404 (Página no encontrada).
    Se ejecuta cuando un usuario intenta acceder a una ruta que no existe.
    """
    flash('La página que buscas no existe.', 'info')  # Mensaje flash informativo.
    return render_template('errors/404.html'), 404  # Renderiza la plantilla de error 404.

# ⚙️ Error 500: Error interno del servidor.
@errorsBp.app_errorhandler(500)
def internal_server_error(error):
    """
    Manejador de errores para el código 500 (Error interno del servidor).
    Se ejecuta cuando ocurre un error inesperado en el servidor.
    """
    # Registra el error en el archivo de logs de la aplicación.
    current_app.logger.error(f"Error 500: {error}")
    
    # Muestra un mensaje flash para notificar al usuario.
    flash('Ocurrió un error interno en el servidor.', 'danger')

    # Renderiza la plantilla de error 500 y retorna el código de estado HTTP 500.
    return render_template('errors/500.html'), 500

"""
🔧 PUNTOS IMPORTANTES:
- `app_errorhandler()`: Decorador para registrar funciones que manejarán errores específicos.
- `flash()`: Muestra un mensaje temporal que será visible en la próxima carga de la página.
- `redirect()`: Redirige a una ruta específica.
- `render_template()`: Renderiza una plantilla HTML.
- `current_app.logger.error()`: Registra un error en los logs de la aplicación.

📌 ¿Cómo añadir más manejadores de errores?
- Para manejar un nuevo error, crea una nueva función usando el decorador `@errorsBp.app_errorhandler(codigo_error)`.
  Por ejemplo, para manejar el error 502 (Bad Gateway):

  @errorsBp.app_errorhandler(502)
  def bad_gateway_error(error):
      flash('Error 502: Problema con el servidor.', 'danger')
      return render_template('errors/502.html'), 502

💡 RECOMENDACIÓN:
- Asegúrate de tener plantillas HTML personalizadas para cada error que manejes.
  Estas plantillas deben estar ubicadas en la carpeta `templates/errors/`.

"""

