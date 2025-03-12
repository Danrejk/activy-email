from sqlite3 import Error
from src.database.utils.rowsToDictionary import rowsToDictionary

def getPlaceById(connection, placeId):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM places WHERE id = ?", (placeId,))
        return rowsToDictionary(cursor, cursor.fetchone())
    except Error as e:
        print(f"Error fetching place by id: {e}")
        return None