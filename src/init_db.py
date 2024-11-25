'''import mysql.connector

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

DB_USERNAME = "root"
DB_PASSWORD = "password_sql"
DB_HOST = "localhost"

DB_NAME = "travel_planner"
'''

import sqlite3

# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect('travel_planner.db')
cursor = conn.cursor()

# Create Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
''')

# Create Trips table
cursor.execute('''
CREATE TABLE IF NOT EXISTS trips (
    trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    destination TEXT,
    start_date TEXT,
    end_date TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
''')

# Create Itineraries table
cursor.execute('''
CREATE TABLE IF NOT EXISTS itineraries (
    itinerary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id INTEGER,
    day INTEGER,
    activity TEXT,
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id)
);
''')

# Commit changes and close the connection
conn.commit()
conn.close()

import sqlite3

# Function to register a new user
def register_user(username, password):
    conn = sqlite3.connect('travel_planner.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO users (username, password) 
    VALUES (?, ?)
    ''', (username, password))
    
    conn.commit()
    conn.close()
    print(f"User '{username}' registered successfully!")

# Function to log in a user
def login_user(username, password):
    conn = sqlite3.connect('travel_planner.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM users WHERE username = ? AND password = ?
    ''', (username, password))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        print(f"Welcome, {user[1]}!")
        return user[0]  # Return user_id
    else:
        print("Invalid login credentials.")
        return None

# Function to log a trip for a user
def log_trip(user_id, destination, start_date, end_date):
    conn = sqlite3.connect('travel_planner.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO trips (user_id, destination, start_date, end_date) 
    VALUES (?, ?, ?, ?)
    ''', (user_id, destination, start_date, end_date))

    conn.commit()
    conn.close()
    print(f"Trip to {destination} logged successfully!")

# Function to add an activity to the itinerary for a trip
def add_itinerary(trip_id, day, activity):
    conn = sqlite3.connect('travel_planner.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO itineraries (trip_id, day, activity) 
    VALUES (?, ?, ?)
    ''', (trip_id, day, activity))
    
    conn.commit()
    conn.close()
    print(f"Activity for day {day} added to itinerary.")

# Function to display a user's trips
def view_trips(user_id):
    conn = sqlite3.connect('travel_planner.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM trips WHERE user_id = ?
    ''', (user_id,))
    
    trips = cursor.fetchall()
    
    if trips:
        print("\nYour Trips:")
        for trip in trips:
            print(f"Trip ID: {trip[0]}, Destination: {trip[2]}, Dates: {trip[3]} to {trip[4]}")
    else:
        print("No trips found.")
    
    conn.close()

def main():
    print("Welcome to the Travel Planner!")
    
    # User Registration and Login
    action = input("Do you want to (1) Register or (2) Login? ")
    
    if action == '1':
        username = input("Enter username: ")
        password = input("Enter password: ")
        register_user(username, password)
    elif action == '2':
        username = input("Enter username: ")
        password = input("Enter password: ")
        user_id = login_user(username, password)
        
        if user_id:
            while True:
                print("\nOptions:")
                print("1. Log a new trip")
                print("2. Add activity to itinerary")
                print("3. View your trips")
                print("4. Logout")
                
                choice = input("Choose an option: ")
                
                if choice == '1':
                    destination = input("Enter destination: ")
                    start_date = input("Enter start date (YYYY-MM-DD): ")
                    end_date = input("Enter end date (YYYY-MM-DD): ")
                    log_trip(user_id, destination, start_date, end_date)
                elif choice == '2':
                    trip_id = int(input("Enter trip ID to add activity to: "))
                    day = int(input("Enter day number: "))
                    activity = input("Enter activity: ")
                    add_itinerary(trip_id, day, activity)
                elif choice == '3':
                    view_trips(user_id)
                elif choice == '4':
                    print("Logging out...")
                    break
                else:
                    print("Invalid option, try again.")
        else:
            print("Invalid login credentials.")
    else:
        print("Invalid option. Exiting.")
    
if __name__ == "__main__":
    main()
