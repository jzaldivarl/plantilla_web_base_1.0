# admin_default_generator.py #

#import sys
#import os

# Agregar la ruta al directorio raíz del proyecto
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db, bcrypt
from app.models import User

# Crear la app de Flask
app = create_app()

# esrciba los campos del usuario que va a crear en la BD
user = 'admin'
numero = 2
generic_user = f'{user}{numero}'
generic_email = f'{user}{numero}@example.com'
generic_password = 'admin123'
generic_is_admin = True
generic_is_verified = True

with app.app_context():

    try:
        # Buscar el usuario
        user = User.query.filter_by(username=generic_user).first()

        if user:
            # Si existe, eliminarlo
            db.session.delete(user)
            db.session.commit()
            print(f"Usuario {generic_user} eliminado.")

        # Crear un nuevo usuario
        new_user = User(
            username=generic_user,
            email=generic_email,
            password_hash=bcrypt.generate_password_hash(generic_password).decode('utf-8'),
            is_admin=generic_is_admin,
            is_verified=generic_is_verified
        )

        db.session.add(new_user)
        db.session.commit()
        print(f"usuario {generic_user} creado con éxito.")

    except Exception as e:
        print(f'Ha ocurrido el siguiente Error:\n\n {str(e)} \n\n intente solucionarlo y pruebe otra vez')


