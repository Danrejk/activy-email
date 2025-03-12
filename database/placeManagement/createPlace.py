from sqlite3 import Error

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
