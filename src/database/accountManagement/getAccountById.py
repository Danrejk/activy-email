from sqlite3 import Error

from src.database.utils.rowsToDictionary import rowsToDictionary

def getAccountById(connection, accountId):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM accounts WHERE id = ?", (accountId,))
        return rowsToDictionary(cursor, cursor.fetchone())
    except Error as e:
        print(f"Error fetching account by id: {e}")
        return None