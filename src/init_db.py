import mysql.connector

import config


def connect_to_mysql():
    try:
        # Establish a connection to the MySQL server
        conn = mysql.connector.connect(
            host=config.DB_HOST, user=config.DB_USERNAME, password=config.DB_PASSWORD
        )
        cursor = conn.cursor()

        # Check if the database exists
        cursor.execute("SHOW DATABASES")
        existing_databases = [row[0] for row in cursor.fetchall()]

        if config.DB_NAME not in existing_databases:
            # Create the database if it doesn't exist
            cursor.execute(f"CREATE DATABASE {config.DB_NAME}")
            print(f"Database '{config.DB_NAME}' created successfully!")

        # Close cursor and connection to the MySQL server
        cursor.close()
        conn.close()

        # Connect to the specific database
        conn = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USERNAME,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
        )
        print(f"Connected to MySQL database '{config.DB_NAME}'")

        return conn

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_table(cursor, table_name, table_desc):
    create_table_cmd = "CREATE TABLE IF NOT EXISTS " f"{table_name} ({table_desc})"
    print(f" [ SQL_CMD ] {create_table_cmd}")
    cursor.execute(create_table_cmd)
    return cursor


conn = connect_to_mysql()
if conn:
    cursor = conn.cursor()

    # Create test_table1
    cursor = create_table(
        cursor=cursor,
        table_name="test_table1",
        table_desc=" ,".join(
            ("id INT AUTO_INCREMENT PRIMARY KEY", "name VARCHAR(255)")
        ),
    )

    # Create test_table2
    cursor = create_table(
        cursor=cursor,
        table_name="test_table2",
        table_desc=" ,".join(
            ("id INT AUTO_INCREMENT PRIMARY KEY", "name VARCHAR(255)", "password VARCHAR(255)", "age INT")
        ),
    )

    conn.commit()
    cursor.close()
    conn.close()
    print("MySQL connection is closed")
else:
    print("Connection to MySQL failed")
