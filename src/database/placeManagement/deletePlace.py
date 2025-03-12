from sqlite3 import Error

def deletePlace(connection, placeId):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM places WHERE id = ?", (placeId,))
        connection.commit()
        print(f"Place with id {placeId} removed successfully.")
    except Error as e:
        print(f"Error removing place: {e}")
