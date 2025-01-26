import psycopg2

#import sys
#import os

# Add the path to the project's root directory
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def execute_query(query, params=None):
    """
    Executes an SQL query on PostgreSQL.

    :param query: SQL query as a string.
    :param params: Optional parameters for the query.
    """
    try:
        # Connect to the database
        connection = psycopg2.connect(
            dbname="database_name",
            user="user",
            password="password",
            host="localhost",
            port=5432
        )
        cursor = connection.cursor()

        # Execute query
        cursor.execute(query, params)
        if query.strip().lower().startswith("select"):
            results = cursor.fetchall()
            for row in results:
                print(row)
        else:
            connection.commit()
            print("Query executed successfully.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close connection
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    # Write your query here
    query = "SELECT * FROM table_name;"
    execute_query(query)

