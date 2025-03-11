from sqlite3 import Error

from database.utils.rowsToDictionary import rowsToDictionary


def createPlace(connection, name, latitude, longitude, workplace=False):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO places (name, latitude, longitude, workplace)
            VALUES (?, ?, ?, ?)
        """, (name, latitude, longitude, workplace))
        connection.commit()
        placeId = cursor.lastrowid
        print(f"Place '{name}' created successfully with id {placeId}.")
        return placeId
    except Error as e:
        print(f"Error creating place: {e}")
        return None

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

def getPlaceById(connection, placeId):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM places WHERE id = ?", (placeId,))
        return rowsToDictionary(cursor, cursor.fetchone())
    except Error as e:
        print(f"Error fetching place by id: {e}")
        return None

def getAllWorkplaces(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM places WHERE workplace = 1")
        return rowsToDictionary(cursor, cursor.fetchall())
    except Error as e:
        print(f"Error fetching workplaces: {e}")
        return []

def getAllNonWorkplaces(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM places WHERE workplace = 0")
        return rowsToDictionary(cursor, cursor.fetchall())
    except Error as e:
        print(f"Error fetching non-workplaces: {e}")
        return []


def updatePlace(connection, placeId, newName=None, newLatitude=None, newLongitude=None, newWorkplace=None):
    try:
        cursor = connection.cursor()
        updates = []
        params = []

        if newName is not None:
            updates.append("name = ?")
            params.append(newName)
        if newLatitude is not None:
            updates.append("latitude = ?")
            params.append(newLatitude)
        if newLongitude is not None:
            updates.append("longitude = ?")
            params.append(newLongitude)
        if newWorkplace is not None:
            updates.append("workplace = ?")
            params.append(newWorkplace)

        if not updates:
            print("No update parameters provided; nothing to change.")
            return

        query = f"UPDATE places SET {', '.join(updates)} WHERE id = ?"
        params.append(placeId)
        cursor.execute(query, tuple(params))
        connection.commit()
        print(f"Place with id {placeId} updated successfully.")
    except Error as e:
        print(f"Error updating place: {e}")

def deletePlace(connection, placeId):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM places WHERE id = ?", (placeId,))
        connection.commit()
        print(f"Place with id {placeId} removed successfully.")
    except Error as e:
        print(f"Error removing place: {e}")
