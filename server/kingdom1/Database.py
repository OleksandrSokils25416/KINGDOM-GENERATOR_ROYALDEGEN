import psycopg2
from datetime import datetime, timedelta
import time

# Database connection settings
DATABASE_CONFIG = {
    "dbname": "royaldegen",
    "user": "postgres",
    "password": "12345",
    "host": "localhost",
    "port": "6575"
}

# Tariff constants
TARIFFS = {
    "free": {
        "id": 1,
        "name": "Free",
        "tokens": "limited",
        "parameters": False,
        "data_usage": True,
        "monthly_price": 0,
        "annual_price": 0
    },
    "paid": {
        "id": 2,
        "name": "Paid",
        "tokens": "unlimited",
        "parameters": False,
        "data_usage": True,
        "monthly_price": 4.99,
        "annual_price": 59.99
    },
    "premium": {
        "id": 3,
        "name": "Premium",
        "tokens": "unlimited",
        "parameters": True,
        "data_usage": True,
        "monthly_price": 9.99,
        "annual_price": 99.99
    },
    "business": {
        "id": 4,
        "name": "Business",
        "tokens": "unlimited",
        "parameters": True,
        "data_usage": False,
        "monthly_price": 14.99,
        "annual_price": 149.99
    }
}


def create_tables():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    # Create users table
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        tariff_id INTEGER,
        status VARCHAR(50) DEFAULT 'inactive',
        FOREIGN KEY (tariff_id) REFERENCES tariffs (id)
    );
    """

    # Create tariffs table
    create_tariffs_table = """
    CREATE TABLE IF NOT EXISTS tariffs (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        monthly_price DECIMAL(10, 2),
        annual_price DECIMAL(10, 2),
        description TEXT
    );
    """

    # Create orders table
    create_orders_table = """
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        tariff_id INTEGER NOT NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        end_date TIMESTAMP,
        status VARCHAR(50) DEFAULT 'active',
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (tariff_id) REFERENCES tariffs (id) ON DELETE SET NULL
    );
    """

    # Execute table creation
    cursor.execute(create_users_table)
    cursor.execute(create_tariffs_table)
    cursor.execute(create_orders_table)

    # Commit and close connection
    conn.commit()
    cursor.close()
    conn.close()
    print("Tables created successfully.")


def initialize_tariffs():
    """
    Inserts predefined tariff plans into the tariffs table if they do not already exist.
    """
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    for tariff in TARIFFS.values():
        insert_tariff_query = """
        INSERT INTO tariffs (id, name, price, monthly_price, annual_price, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """
        description = (
            f"Tokens: {tariff['tokens']}, Parameters: {tariff['parameters']}, Data Usage: {tariff['data_usage']}, "
            f"Monthly: ${tariff['monthly_price']}, Annual: ${tariff['annual_price']}")
        cursor.execute(insert_tariff_query, (
            tariff['id'],
            tariff['name'],
            tariff['monthly_price'],
            tariff['monthly_price'],
            tariff['annual_price'],
            description
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("Tariff plans initialized.")


def check_and_update_subscriptions():
    """
    Checks for expired subscriptions daily and updates user status accordingly.
    """
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    # Query to find expired subscriptions
    check_expired_query = """
    SELECT id, user_id FROM orders
    WHERE end_date <= NOW() AND status = 'active';
    """
    cursor.execute(check_expired_query)
    expired_orders = cursor.fetchall()

    # Update the status of expired subscriptions and reset to free tier
    for order_id, user_id in expired_orders:
        print(f"Subscription expired for user_id {user_id}, order_id {order_id}. Resetting to Free.")
        update_order_status = """
        UPDATE orders SET status = 'expired' WHERE id = %s;
        """
        update_user_tariff = """
        UPDATE users SET tariff_id = %s WHERE id = %s;
        """
        cursor.execute(update_order_status, (order_id,))
        cursor.execute(update_user_tariff, (TARIFFS['free']['id'], user_id))
        conn.commit()

    cursor.close()
    conn.close()
    print("Subscription statuses updated.")


def purchase_subscription(user_id, tariff_name, duration_days):
    """
    Purchases a subscription for a user, assigns a tariff, and creates an order.
    """
    if tariff_name not in TARIFFS:
        print("Invalid tariff name.")
        return

    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    # Set end_date based on duration
    end_date = datetime.now() + timedelta(days=duration_days)

    # Insert new order
    create_order_query = """
    INSERT INTO orders (user_id, tariff_id, end_date, status)
    VALUES (%s, %s, %s, 'active');
    """
    update_user_tariff_query = """
    UPDATE users SET tariff_id = %s WHERE id = %s;
    """

    tariff_id = TARIFFS[tariff_name]['id']
    cursor.execute(create_order_query, (user_id, tariff_id, end_date))
    cursor.execute(update_user_tariff_query, (tariff_id, user_id))
    conn.commit()

    cursor.close()
    conn.close()
    print(f"Subscription '{tariff_name}' purchased successfully for user_id {user_id}.")


def main():
    """
    Main function to initialize tariffs and manage subscriptions.
    """
    create_tables()
    initialize_tariffs()



if __name__ == "__main__":
    main()
