from sqlite3 import Error

def createPlace(connection, name, latitude, longitude, workplace=False):
    """
    Create a new place with the given parameters.
    Returns the id of the newly created place.
    """
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

def getPlaceById(connection, placeId):
    """
    Fetch and return the place corresponding to the given placeId.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM places WHERE id = ?", (placeId,))
        place = cursor.fetchone()
        if place:
            print(f"Place found: {place}")
        else:
            print(f"No place found with id: {placeId}")
        return place
    except Error as e:
        print(f"Error fetching place by id: {e}")
        return None

def isWorkplace(connection, placeId):
    """
    Return True if the place with the given id is marked as a workplace,
    otherwise return False.
    """
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

def getAllWorkplaces(connection):
    """
    Fetch and return all places where workplace is True.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM places WHERE workplace = 1")
        workplaces = cursor.fetchall()
        print(f"Fetched {len(workplaces)} workplace(s).")
        return workplaces
    except Error as e:
        print(f"Error fetching workplaces: {e}")
        return []

def getAllNonWorkplaces(connection):
    """
    Fetch and return all places where workplace is False.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM places WHERE workplace = 0")
        nonWorkplaces = cursor.fetchall()
        print(f"Fetched {len(nonWorkplaces)} non-workplace place(s).")
        return nonWorkplaces
    except Error as e:
        print(f"Error fetching non-workplaces: {e}")
        return []

def updatePlace(connection, placeId, newName=None, newLatitude=None, newLongitude=None, newWorkplace=None):
    """
    Update place details for the place with the given placeId.
    Only provided new values will be updated.
    """
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
    """
    Remove the place with the given placeId from the database.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM places WHERE id = ?", (placeId,))
        connection.commit()
        print(f"Place with id {placeId} removed successfully.")
    except Error as e:
        print(f"Error removing place: {e}")
