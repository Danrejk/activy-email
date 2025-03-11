from sqlite3 import Error

from database.utils.rowsToDictionary import rowsToDictionary


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

def getChallengeById(connection, challengeId):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM challenges WHERE id = ?", (challengeId,))
        return rowsToDictionary(cursor, cursor.fetchone())
    except Error as e:
        print(f"Error fetching challenge by id: {e}")
        return None

def getAllChallenges(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM challenges")
        return rowsToDictionary(cursor, cursor.fetchall())
    except Error as e:
        print(f"Error fetching challenges: {e}")
        return []

def updateChallenge(connection, challengeId, newName=None, newStartDate=None, newEndDate=None):
    try:
        cursor = connection.cursor()
        updates = []
        params = []

        if newName is not None:
            updates.append("name = ?")
            params.append(newName)
        if newStartDate is not None:
            updates.append("startDate = ?")
            params.append(newStartDate)
        if newEndDate is not None:
            updates.append("endDate = ?")
            params.append(newEndDate)

        if not updates:
            print("No update parameters provided; nothing to change.")
            return

        query = f"UPDATE challenges SET {', '.join(updates)} WHERE id = ?"
        params.append(challengeId)
        cursor.execute(query, tuple(params))
        connection.commit()
        print(f"Challenge with id {challengeId} updated successfully.")
    except Error as e:
        print(f"Error updating challenge: {e}")

def deleteChallenge(connection, challengeId):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM challenges WHERE id = ?", (challengeId,))
        connection.commit()
        print(f"Challenge with id {challengeId} removed successfully.")
    except Error as e:
        print(f"Error removing challenge: {e}")
