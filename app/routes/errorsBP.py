# app/routes/errorsBP.py

# 📋 Routes for managing application errors in Flask.

from flask import Blueprint, render_template, redirect, url_for, flash, current_app

# 🧩 Create a blueprint named 'errors' that groups error handlers.
# This helps organize error controllers in a separate module.
errorsBp = Blueprint('errors', __name__)

# ✅ Common function to handle errors and redirect to login.
# This centralizes the redirection logic for common errors.
def handle_common_errors(error, message, category):
    """
    Displays a flash message with the specified category and redirects to the login view.

    - error: Captured error object.
    - message: Message to be displayed to the user.
    - category: Message category (info, warning, danger).
    """
    flash(message, category)  # Displays a flash message to the user.
    return redirect(url_for('loginBP.login_view'))  # Redirects to the login view.

# ⚠️ Specific error handling with respective controller functions.

# 🛑 Error 401: Unauthorized.
@errorsBp.app_errorhandler(401)
def unauthorized_error(error):
    """
    Error handler for 401 (Unauthorized).
    Triggered when a user attempts to access a protected route without authentication.
    """
    return handle_common_errors(error, 'Unauthorized. Please log in.', 'warning')

# 🛡️ Error 400: Bad request (e.g., CSRF failure).
@errorsBp.app_errorhandler(400)
def handle_bad_request(error):
    """
    Error handler for 400 (Bad Request).
    Triggered when Flask detects a security-related issue,
    such as a missing or invalid CSRF token.
    """
    flash('Security error: missing or invalid CSRF token.')  # Flash error message.
    return render_template('errors/400.html'), 400  # Renders the error 400 template.

# 🚫 Error 403: Forbidden.
@errorsBp.app_errorhandler(403)
def forbidden_error(error):
    """
    Error handler for 403 (Forbidden).
    Triggered when a user attempts to access a route without sufficient permissions.
    """
    return handle_common_errors(error, 'Access denied. You do not have the necessary permissions.', 'danger')

# 🔍 Error 404: Page not found.
@errorsBp.app_errorhandler(404)
def not_found_error(error):
    """
    Error handler for 404 (Page Not Found).
    Triggered when a user attempts to access a non-existent route.
    """
    flash('The page you are looking for does not exist.', 'info')  # Flash info message.
    return render_template('errors/404.html'), 404  # Renders the error 404 template.

# ⚙️ Error 500: Internal server error.
@errorsBp.app_errorhandler(500)
def internal_server_error(error):
    """
    Error handler for 500 (Internal Server Error).
    Triggered when an unexpected server error occurs.
    """
    # Logs the error in the application logs.
    current_app.logger.error(f"Error 500: {error}")

    # Displays a flash message to notify the user.
    flash('An internal server error occurred.', 'danger')

    # Renders the error 500 template and returns the HTTP 500 status code.
    return render_template('errors/500.html'), 500

"""
🔧 KEY POINTS:
- `app_errorhandler()`: Decorator to register functions that handle specific errors.
- `flash()`: Displays a temporary message visible on the next page load.
- `redirect()`: Redirects to a specific route.
- `render_template()`: Renders an HTML template.
- `current_app.logger.error()`: Logs an error in the application logs.

📌 How to add more error handlers?
- To handle a new error, create a new function using the decorator `@errorsBp.app_errorhandler(error_code)`.
  For example, to handle a 502 (Bad Gateway) error:

  @errorsBp.app_errorhandler(502)
  def bad_gateway_error(error):
      flash('Error 502: Server issue.', 'danger')
      return render_template('errors/502.html'), 502

"""


