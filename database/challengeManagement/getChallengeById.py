from sqlite3 import Error
from database.utils.rowsToDictionary import rowsToDictionary

def getChallengeById(connection, challengeId):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM challenges WHERE id = ?", (challengeId,))
        return rowsToDictionary(cursor, cursor.fetchone())
    except Error as e:
        print(f"Error fetching challenge by id: {e}")
        return None