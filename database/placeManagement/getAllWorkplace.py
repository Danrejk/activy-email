from sqlite3 import Error
from database.utils.rowsToDictionary import rowsToDictionary

def getAllWorkplaces(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM places WHERE workplace = 1")
        return rowsToDictionary(cursor, cursor.fetchall())
    except Error as e:
        print(f"Error fetching workplaces: {e}")
        return []