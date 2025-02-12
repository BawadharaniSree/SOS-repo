def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',       # Replace with your host
            database='sos_app',     # Replace with your database name
            user='root',            # Replace with your username
            password='Vasu3024.' # Replace with your password
        )
        if connection.is_connected():
            print("Database connection successful!")
            return connection
        else:
            print("Failed to connect to the database.")
            return None
    except Error as e:
        print(f"Error: {e}")
        return None