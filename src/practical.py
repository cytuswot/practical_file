import mysql.connector
import config

def connect_to_mysql():
	conn = mysql.connector.connect(host = config.DB_HOST, user = config.DB_USER, database = config.DB_NAME, password = config.DB_PASSWORD)
	cursor = conn.cursor()
	
	# Check if the database exixts
	cursor.execute("show databases;")
	
	existing_databases = [row[0] for row in cursor.fetchall()]
	
	if config.DB_NAME not in existing_databases:
		
		# Create the database if it doesn't exist
		cursor.execute(f"create database {config.DB_NAME}")
		
		print(f"Database '{config.DB_NAME}' created successfully")
		
	# Create users table
	cursor.execute('''create table if not exists users(
		user_id int primary key auto_increment,
		username varchar(20),
		password varchar(15)
		);''')
	
	# Create trips table
	cursor.execute('''create table if not exists trips(
		trip_id int primary key auto_increment,
		user_id int,
		destination varchar(20),
		start_date date,
		end_date date,
		foreign key(user_id) references users(user_id)
		);''')
		
	# Create itineraries table
	cursor.execute('''create table if not exists itineraries(
		itinerary_id int primary key auto_increment,
		trip_id int,
		activity varchar(100),
		foreign key(trip_id) references trips(trip_id)
		);''')
		
	# Close cursor and connection to the MySql server
	cursor.close()
	conn.close()
connect_to_mysql()

import mysql.connector

# Function to register a new user
def register_user(username,password):
	conn = mysql.connector.connect(host = config.DB_HOST, user = config.DB_USER, database = config.DB_NAME, password = config.DB_PASSWORD)
	cursor = conn.cursor()
	
	cursor.execute('''insert into users(username,password)
		values(%s,%s)''' , (username,password))
	
	conn.commit()
	conn.close()
	
	print(f"User '{username}' registered successfully")

# Function to log in a user
def login_user(username,password):
	conn = mysql.connector.connect(host = config.DB_HOST, user = config.DB_USER, database = config.DB_NAME, password = config.DB_PASSWORD)
	cursor = conn.cursor()
	
	cursor.execute('''select * from users 
		where username = %s and password = %s''',
		(username,password))
	
	user = cursor.fetchone()
	
	conn.close()
	
	if user:
		print(f"Welcome, {user[1]}")
		return user[0]       # Return user_id
	
	else:
		print("Invalid login... Please check username or password and try again!")
		return None
		
# Function to log a trip 
def log_trip(user_id,destination,start_date,end_date):
	conn = mysql.connector.connect(host = config.DB_HOST, user = config.DB_USER, database = config.DB_NAME, password = config.DB_PASSWORD)
	cursor = conn.cursor()
	
	cursor.execute('''insert into trips(user_id,destination,start_date,end_date)
		values(%s, %s, %s, %s)''', (user_id,destination,start_date,end_date))
	
	conn.commit()
	conn.close()
	
	print(f"Trip to '{destination}' logged successfully")

# Function to add an activity to the itinerary for a trip
def add_itinerary(trip_id,activity):
	conn = mysql.connector.connect(host = config.DB_HOST, user = config.DB_USER, database = config.DB_NAME, password = config.DB_PASSWORD)
	cursor = conn.cursor()
	
	cursor.execute('''insert into itineraries(trip_id,activity)
			values(%s, %s)''', (trip_id,activity))
	
	conn.commit()
	conn.close()
	
	print("Activity added to itinerary")

# Function to display user's trips
def view_trips(user_id):
	conn = mysql.connector.connect(host = config.DB_HOST, user = config.DB_USER, database = config.DB_NAME, password = config.DB_PASSWORD)
	cursor = conn.cursor()
	
	cursor.execute('''select * from trips
				where user_id = %s''', (user_id,))
	
	trips = cursor.fetchall()
	
	if trips:
		print("\nYour Trips:")
		for trip in trips:
			print(f"Trip ID: {trip[0]} , Destination: {trip[2]}, Dates: {trip[3]} to {trip[4]}")
	
	else:
		print("No trips found!")
	
	conn.close()

def main_menu():
	print("Welcome to the Travel Planner")
	 
	action = input("Do you want to: (1)Register or (2)Login? ---> ")
	 
	if action == "1":
		 username = input("Enter username: ")
		 password = input("Enter password: ")
		 register_user(username,password)
		 
	elif action == "2":
		username = input("Enter username: ")
		password = input("Enter password: ")
		user_id = login_user(username,password)
		
		if user_id:
			while True:
				print("\nOptions:")
				print("1. Log a new trip")
				print("2. Add activity to itinerary")
				print("3. View your trips")
				print("4. Logout")
				
				choice = input("Choose an option from above: ")
				
				if choice == "1":
					destination = input("Enter destination: ")
					start_date = input("Enter start date (YYYY-MM-DD): ")
					end_date = input("Enter end date (YYYY-MM-DD): ")
					log_trip(user_id, destination, start_date, end_date)
				
				elif choice == '2':
					trip_id = int(input("Enter trip ID to add activity to: "))
					activity = input("Enter activity: ")
					add_itinerary(trip_id, activity)
				
				elif choice == '3':
					view_trips(user_id)
				
				elif choice == '4':
					print("Logging out...")
					break
				
				else:
					print("Invalid option, try again.")

main_menu()
					
				
