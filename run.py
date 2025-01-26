# run.py - # Main file to run the Flask application

# Import the function to create the app instance
from app import create_app

# Create an instance of the Flask application
# using the function defined in app/__init__.py
app = create_app()

# Application entry point
if __name__ == '__main__':
    # Run the application in debug mode (useful for development)
    app.run(debug=True)

    # If you want to change the IP address or port, you can do so here.
    # app.run(debug=True, host='0.0.0.0', port=5000)

    """
    📌 Available parameters for the run() method:
    - `host`: Specifies the IP address where the app will run.
      By default, it is '127.0.0.1' (localhost). If you want the app to be accessible
      from other machines on the network, change the value to '0.0.0.0'.

      Example:
      app.run(host='0.0.0.0')

    - `port`: Specifies the port the application will listen to.
      The default value is 5000, but you can change it to any available port.

      Example:
      app.run(port=8080)

    - `debug`: Activates debug mode for development. This allows the app to automatically reload
      when it detects changes in the files. Useful during development.

      Example:
      app.run(debug=True)

    - `use_reloader`: Controls whether the app should restart automatically when file changes are detected.
      It is useful during development but can be disabled in production.

      Example:
      app.run(use_reloader=False)

    ✅ Recommendation for local network development:
    If you want your application to be accessible from other devices on your local network,
    run the app with the following parameters:

    app.run(host='0.0.0.0', port=5000, debug=True)

    This will make the app available on your machine's local IP address (e.g., 192.168.1.x),
    and any device on the same network will be able to access it using that IP address.
    """


