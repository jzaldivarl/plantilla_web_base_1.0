# change_password.py

'''
 Instrucciones para usar el script:

    Guarda el archivo como change_password.py.
    Modifica los valores en dbname, user, password, target_user, y new_password según tus necesidades.
    Ejecuta el script:
    python change_password.py
'''

import psycopg2
from psycopg2 import sql

def change_password(dbname, user, password, target_user, new_password):
    """
    Cambia la contraseña de un usuario en PostgreSQL.

    :param dbname: Nombre de la base de datos.
    :param user: Usuario con privilegios (como 'postgres').
    :param password: Contraseña del usuario.
    :param target_user: Usuario al que se le cambiará la contraseña.
    :param new_password: Nueva contraseña para el usuario objetivo.
    """
    try:
        # Conexión a PostgreSQL
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host="localhost",
            port=5432
        )
        connection.autocommit = True  # Asegura que los cambios se guarden de inmediato

        # Crear un cursor para ejecutar comandos
        cursor = connection.cursor()

        # Cambiar la contraseña
        cursor.execute(sql.SQL("ALTER USER {} WITH PASSWORD %s").format(
            sql.Identifier(target_user)),
            [new_password]
        )

        print(f"Contraseña de '{target_user}' actualizada exitosamente.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Cerrar conexión
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    # Configuración
    dbname = "postgres"  # Cambia esto según tu base de datos
    user = "postgres"
    password = "tu_contraseña_actual"
    target_user = "postgres"  # Usuario al que deseas cambiar la contraseña
    new_password = "nueva_contraseña_segura"

    # Cambiar contraseña
    change_password(dbname, user, password, target_user, new_password)
