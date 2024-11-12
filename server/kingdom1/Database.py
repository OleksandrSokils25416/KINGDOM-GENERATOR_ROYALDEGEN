import psycopg2
from psycopg2 import sql

# Database connection settings
DATABASE_CONFIG = {
    "dbname": "royaldegen",
    "user": "postgres",
    "password": "12345",
    "host": "localhost",
    "port": "6575"
}

# Function to create users table if it doesn't exist
def create_tables():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL
    );
    """
    cursor.execute(create_users_table)
    conn.commit()
    cursor.close()
    conn.close()
    print("Tables created successfully if they didn't exist.")

# Run the function to ensure tables are set up
if __name__ == "__main__":
    create_tables()
