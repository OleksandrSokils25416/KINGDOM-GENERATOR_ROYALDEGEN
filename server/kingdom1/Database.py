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

# Function to create tables
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
        temperature FLOAT CHECK (temperature >= 0 AND temperature <= 1),
        max_tokens INTEGER,
        generated_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    # Create subscription_plans table
    create_subscription_plans_table = """
    CREATE TABLE IF NOT EXISTS subscription_plans (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        duration_days INTEGER NOT NULL,
        description TEXT,
        max_words INTEGER,
        access_to_best_model BOOLEAN DEFAULT FALSE
    );
    """

    # Create user_subscriptions table
    create_user_subscriptions_table = """
    CREATE TABLE IF NOT EXISTS user_subscriptions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        plan_id INTEGER REFERENCES subscription_plans(id),
        start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        end_date TIMESTAMP NOT NULL
    );
    """

    cursor.execute(create_users_table)
    cursor.execute(create_prompts_table)
    cursor.execute(create_subscription_plans_table)
    cursor.execute(create_user_subscriptions_table)
    conn.commit()
    cursor.close()
    conn.close()
    print("Tables created successfully if they didn't exist.")

def create_default_subscription_plans():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    # Insert default subscription plans
    default_plans = [
        ("Basic", 0.00, 30, "Basic plan with limited features: max 100 characters and temperature up to 0.5.", 100, False),
        ("Premium", 9.99, 30, "Premium plan with unlimited access to all features.", None, True),
        ("Admin", 0.00, 3650, "Administrative plan with access to all features and endpoints.", None, True)
    ]

    for plan in default_plans:
        cursor.execute(
            """
            INSERT INTO subscription_plans (name, price, duration_days, description, max_words, access_to_best_model)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (name) DO NOTHING;
            """,
            plan
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("Default subscription plans created successfully.")

def create_test_data():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    # Insert test users
    test_users = [
        ("user1", "user1@example.com", "hashed_password1"),
        ("user2", "user2@example.com", "hashed_password2"),
        ("admin", "admin@example.com", "hashed_password3")
    ]

    for user in test_users:
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
            ON CONFLICT (username) DO NOTHING;
            """,
            user
        )

    # Assign subscriptions to users
    test_subscriptions = [
        (1, 1, '2025-01-01', '2025-01-31'),  # user1 -> Basic, expires soon
        (2, 2, '2025-01-01', '2025-01-15'),  # user2 -> Premium, already expired
        (3, 3, '2025-01-01', '2035-01-01')   # admin -> Admin, long-term active
    ]

    for user_id, plan_id, start_date, end_date in test_subscriptions:
        cursor.execute(
            """
            INSERT INTO user_subscriptions (user_id, plan_id, start_date, end_date)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
            """,
            (user_id, plan_id, start_date, end_date)
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("Test data created successfully.")

# Function to remove expired subscriptions
def remove_expired_subscriptions():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    # Remove expired subscriptions
    remove_expired_query = """
    DELETE FROM user_subscriptions
    WHERE end_date < CURRENT_TIMESTAMP;
    """
    cursor.execute(remove_expired_query)
    conn.commit()
    cursor.close()
    conn.close()
    print("Expired subscriptions removed successfully.")

# Function to drop all data from tables
def drop_all_data():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    drop_data_query = """
    TRUNCATE TABLE prompts, user_subscriptions, subscription_plans, users RESTART IDENTITY CASCADE;
    """
    cursor.execute(drop_data_query)
    conn.commit()
    cursor.close()
    conn.close()
    print("All data dropped successfully.")

# Function to get a user's current subscription
def get_current_subscription(user_id):
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    query = """
    SELECT sp.name, sp.price, sp.description, sp.max_words, sp.access_to_best_model, us.start_date, us.end_date
    FROM user_subscriptions us
    JOIN subscription_plans sp ON us.plan_id = sp.id
    WHERE us.user_id = %s AND us.end_date >= CURRENT_TIMESTAMP
    ORDER BY us.end_date DESC
    LIMIT 1;
    """
    cursor.execute(query, (user_id,))
    subscription = cursor.fetchone()

    cursor.close()
    conn.close()

    if subscription:
        return {
            "plan_name": subscription[0],
            "price": subscription[1],
            "description": subscription[2],
            "max_words": subscription[3],
            "access_to_best_model": subscription[4],
            "start_date": subscription[5],
            "end_date": subscription[6]
        }
    else:
        return None

# Run the functions
if __name__ == "__main__":
    create_tables()
    drop_all_data()
    create_default_subscription_plans()
    # create_test_data()
    remove_expired_subscriptions()

    # Example usage
    print("Current subscription for user1:", get_current_subscription(1))