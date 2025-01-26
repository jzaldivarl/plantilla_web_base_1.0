# change_password.py

#import sys
#import os

# Add the project root directory to the path
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

'''
 Instructions to use the script:

    Save the file as change_password.py.
    Modify the values in dbname, user, password, target_user, and new_password as needed.
    Run the script:
    python change_password.py
'''

import psycopg2
from psycopg2 import sql

def change_password(dbname, user, password, target_user, new_password):
    """
    Changes the password of a user in PostgreSQL.

    :param dbname: Name of the database.
    :param user: User with privileges (e.g., 'postgres').
    :param password: User's password.
    :param target_user: The user whose password will be changed.
    :param new_password: New password for the target user.
    """
    try:
        # Connect to PostgreSQL
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host="localhost",
            port=5432
        )
        connection.autocommit = True  # Ensure that changes are saved immediately

        # Create a cursor to execute commands
        cursor = connection.cursor()

        # Change the password
        cursor.execute(sql.SQL("ALTER USER {} WITH PASSWORD %s").format(
            sql.Identifier(target_user)),
            [new_password]
        )

        print(f"Password for '{target_user}' successfully updated.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close connection
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":

    # Configuration
    dbname = "postgres"  # Change this to your database name
    user = "postgres"
    password = "your_current_password"
    target_user = "postgres"  # User whose password you want to change
    new_password = "new_secure_password"

    # Change password
    change_password(dbname, user, password, target_user, new_password)

