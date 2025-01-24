from flask_bcrypt import Bcrypt

#import sys
#import os

# Agregar la ruta al directorio raíz del proyecto
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bcrypt = Bcrypt()

# Hash de ejemplo
hashed_password = bcrypt.generate_password_hash("admin123").decode('utf-8')
print(f"Hash generado: {hashed_password}")

# Verificación
is_valid = bcrypt.check_password_hash(hashed_password, "admin123")
print(f"¿Es válida la contraseña? {is_valid}")
