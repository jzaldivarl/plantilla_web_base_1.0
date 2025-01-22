import psycopg2

#import sys
#import os

# Agregar la ruta al directorio raíz del proyecto
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def execute_query(query, params=None):
    """
    Ejecuta una consulta SQL en PostgreSQL.

    :param query: Consulta SQL como cadena.
    :param params: Parámetros opcionales para la consulta.
    """
    try:
        # Conexión a la base de datos
        connection = psycopg2.connect(
            dbname="nombre_base_de_datos",
            user="usuario",
            password="contraseña",
            host="localhost",
            port=5432
        )
        cursor = connection.cursor()

        # Ejecutar consulta
        cursor.execute(query, params)
        if query.strip().lower().startswith("select"):
            results = cursor.fetchall()
            for row in results:
                print(row)
        else:
            connection.commit()
            print("Consulta ejecutada exitosamente.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Cerrar conexión
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    # Escribe tu consulta aquí
    query = "SELECT * FROM nombre_tabla;"
    execute_query(query)
