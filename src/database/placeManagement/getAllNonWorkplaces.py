from sqlite3 import Error
from src.database.utils.rowsToDictionary import rowsToDictionary

def getAllNonWorkplaces(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM places WHERE workplace = 0")
        return rowsToDictionary(cursor, cursor.fetchall())
    except Error as e:
        print(f"Error fetching non-workplaces: {e}")
        return []