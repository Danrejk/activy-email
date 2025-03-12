from sqlite3 import Error

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
