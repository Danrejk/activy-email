from sqlite3 import Error

def isWorkplace(connection, placeId):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT workplace FROM places WHERE id = ?", (placeId,))
        result = cursor.fetchone()
        if result is not None:
            # SQLite doesn't have a native BOOLEAN type; usually 0 is false and 1 is true.
            return bool(result[0])
        else:
            print(f"No place found with id: {placeId}")
            return False
    except Error as e:
        print(f"Error checking if place is a workplace: {e}")
        return False