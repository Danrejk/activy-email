from sqlite3 import Error

def deleteChallenge(connection, challengeId):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM challenges WHERE id = ?", (challengeId,))
        connection.commit()
        print(f"Challenge with id {challengeId} removed successfully.")
    except Error as e:
        print(f"Error removing challenge: {e}")
