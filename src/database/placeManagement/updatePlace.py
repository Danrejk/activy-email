from sqlite3 import Error

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
