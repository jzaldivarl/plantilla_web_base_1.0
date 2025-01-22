# random_password_generator #

#import sys
#import os

# Agregar la ruta al directorio raíz del proyecto
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import secrets
print(secrets.token_urlsafe(32))  # Genera una clave aleatoria

