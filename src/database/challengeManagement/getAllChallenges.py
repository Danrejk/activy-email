from sqlite3 import Error
from src.database.utils.rowsToDictionary import rowsToDictionary

def getAllChallenges(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM challenges")
        return rowsToDictionary(cursor, cursor.fetchall())
    except Error as e:
        print(f"Error fetching challenges: {e}")
        return []