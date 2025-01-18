# run.py - Archivo principal para ejecutar la aplicación Flask

# Importa la función para crear la instancia de la app
from app import create_app

# Crear una instancia de la aplicación Flask
# usando la función definida en app/__init__.py
app = create_app()

# Punto de entrada de la aplicación
if __name__ == '__main__':

    # Ejecuta la aplicación en modo debug (útil para desarrollo)
    # Si deseas cambiar la dirección IP o puerto, puedes hacerlo aquí.
    app.run(debug=True, host='0.0.0.0', port=5000)

    """
    📌 Parámetros disponibles para el método run():
    - `host`: Especifica la dirección IP donde se ejecutará la app.
      Por defecto es '127.0.0.1' (localhost). Si deseas que la app sea accesible desde otras
      máquinas en la red, cambia el valor a '0.0.0.0'.

      Ejemplo:
      app.run(host='0.0.0.0')

    - `port`: Especifica el puerto en el que la aplicación escuchará.
      El valor por defecto es 5000, pero puedes cambiarlo a cualquier puerto disponible.

      Ejemplo:
      app.run(port=8080)

    - `debug`: Activa el modo debug para desarrollo. Esto permite que la app se recargue automáticamente
      al detectar cambios en los archivos. Útil durante el desarrollo.

      Ejemplo:
      app.run(debug=True)

    - `use_reloader`: Controla si la app debe reiniciarse automáticamente cuando se detectan cambios en los archivos.
      Es útil en desarrollo, pero puede ser desactivado en producción.

      Ejemplo:
      app.run(use_reloader=False)

    ✅ Recomendación para desarrollo en red local:
    Si deseas que tu aplicación sea accesible desde otros dispositivos en tu red local,
    ejecuta la app con los siguientes parámetros:

    app.run(host='0.0.0.0', port=5000, debug=True)

    Esto hará que la app esté disponible en la IP local de tu máquina (por ejemplo, 192.168.1.x),
    y cualquier dispositivo en la misma red podrá acceder a ella usando esa dirección IP.
    """

