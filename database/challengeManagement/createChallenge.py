from sqlite3 import Error

def createChallenge(connection, name, startDate=None, endDate=None):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO challenges (name, startDate, endDate)
            VALUES (?, ?, ?)
        """, (name, startDate, endDate))
        connection.commit()
        challengeId = cursor.lastrowid
        print(f"Challenge '{name}' created successfully with id {challengeId}.")
        return challengeId
    except Error as e:
        print(f"Error creating challenge: {e}")
        return None