# run.py #

from app import create_app

# Crear instancia de la app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
