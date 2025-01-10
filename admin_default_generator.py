# admin_default_generator.py #

from app import create_app, db, bcrypt
from app.models import User

# Crear la app de Flask
app = create_app()

with app.app_context():
    # Buscar el usuario admin
    admin_user = User.query.filter_by(username="admin").first()

    if admin_user:
        # Si existe, eliminarlo
        db.session.delete(admin_user)
        db.session.commit()
        print("Usuario 'admin' eliminado.")

    # Crear un nuevo usuario admin
    new_admin_user = User(
        username="admin",
        email="admin@example.com",
        password_hash=bcrypt.generate_password_hash("admin123").decode('utf-8'),
        is_admin=True,
        is_verified=True
    )

    db.session.add(new_admin_user)
    db.session.commit()
    print("Usuario 'admin' creado con éxito.")
