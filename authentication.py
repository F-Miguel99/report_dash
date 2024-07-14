# authentication.py

import sqlite3
import hashlib

DATABASE_FILE = 'users.db'

def create_table():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT NOT NULL UNIQUE,
                      password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    # Check if the username already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print(f"Username {username} already exists.")
        return False  # Or handle appropriately

    # If username does not exist, proceed with registration
    hashed_password = hash_password(password)  # Assuming you have a function to hash the password
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        connection.commit()
        print(f"User {username} registered successfully.")
        return True
    except sqlite3.IntegrityError as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        connection.close()

def authenticate_user(username, password):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user



def delete_user(username):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()


def user_exists(username):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return True if user else False

# authentication.py

# Define a function to check if the user is authenticated
def is_authenticated(username, password):
    user = authenticate_user(username, password)
    return True if user else False



def get_all_users():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users
