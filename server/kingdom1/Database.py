import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
# Database connection settings
DATABASE_CONFIG = {
    "dbname": os.getenv("DBNAME"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
}


# Function to create users table if it doesn't exist
def create_tables():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    # Create users table
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL
    );
    """

    # Create prompts table
    create_prompts_table = """
    CREATE TABLE IF NOT EXISTS prompts (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        prompt TEXT NOT NULL,
        temperature FLOAT,
        max_tokens INTEGER,
        generated_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    cursor.execute(create_users_table)
    cursor.execute(create_prompts_table)
    conn.commit()
    cursor.close()
    conn.close()
    print("Tables created successfully if they didn't exist.")


# Run the function to ensure tables are set up
if __name__ == "__main__":
    create_tables()
