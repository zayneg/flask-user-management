import sqlite3
from config import DATABASE

def get_db_connection():
    conn=sqlite3.connect(DATABASE)
    conn.row_factory=sqlite3.Row
    return conn

def initialize_database():
    conn=get_db_connection()
    conn.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, fullname TEXT NOT NULL, email TEXT UNIQUE NOT NULL, age INTEGER NOT NULL)""")
    conn.commit()
    conn.close()