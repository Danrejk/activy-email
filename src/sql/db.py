import sqlite3
from sqlite3 import Error

class SQLHandler:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.createConnection()

    def createConnection(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            print(f"Connected to {self.db_name}")
        except Error as e:
            print(f"Error connecting to database: {e}")

    def createTables(self):
        try:
            cursor = self.connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS places (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS challenges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    startDate TIMESTAMP,
                    endDate TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    surname TEXT NOT NULL,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    avatar BLOB,
                    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    challengeId INTEGER NOT NULL,
                    points INTEGER NOT NULL DEFAULT 0,
                    homeId INTEGER NOT NULL,
                    workplaceId INTEGER NOT NULL,
                    averageSpeed REAL NOT NULL DEFAULT 20,
                    FOREIGN KEY (challengeId) REFERENCES challenges (id)
                    FOREIGN KEY (homeId) REFERENCES places (id)
                    FOREIGN KEY (workplaceId) REFERENCES places (id)
                )
            """)

            self.connection.commit()
            print("Tables 'accounts' and 'places' created or already exist.")
        except Error as e:
            print(f"Error creating tables: {e}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print(f"Connection to {self.db_name} closed.")

# example usage
createTables = SQLHandler("Activy.db")