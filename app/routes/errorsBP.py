# app/routes/errorsBP.py #

from flask import Blueprint, render_template, redirect, url_for, flash, current_app

# Crea un blueprint llamado 'errors'
errorsBp = Blueprint('errors', __name__)

# Función común para manejar errores y redirigir al login
def handle_common_errors(error, message, category):
    flash(message, category)
    return redirect(url_for('loginBP.login_view'))


# Error 401: No autorizado
@errorsBp.app_errorhandler(401)
def unauthorized_error(error):
    return handle_common_errors(error, 'No autorizado. Por favor, inicia sesión.', 'warning')


# Error handler para capturar el error 400 causado por CSRF
@errorsBp.app_errorhandler(400)
def handle_bad_request(error):
    flash('Error de seguridad: token CSRF faltante o inválido.')
    return render_template('errors/400.html'), 400


# Error 403: Acceso denegado
@errorsBp.app_errorhandler(403)
def forbidden_error(error):
    return handle_common_errors(error, 'Acceso denegado. No tienes los permisos necesarios.', 'danger')


# Error 404: Página no encontrada
@errorsBp.app_errorhandler(404)
def not_found_error(error):
    flash('La página que buscas no existe.', 'info')
    return render_template('errors/404.html'), 404


# Error 500: Error interno del servidor
@errorsBp.app_errorhandler(500)
def internal_server_error(error):
    current_app.logger.error(f"Error 500: {error}")
    flash('Ocurrió un error interno en el servidor.', 'danger')
    return render_template('errors/500.html'), 500
