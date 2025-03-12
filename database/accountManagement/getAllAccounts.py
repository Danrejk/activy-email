from sqlite3 import Error

from database.utils.rowsToDictionary import rowsToDictionary

def getAllAccounts(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM accounts")
        return rowsToDictionary(cursor, cursor.fetchall())
    except Error as e:
        print(f"Error fetching accounts: {e}")
        return []