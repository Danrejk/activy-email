from sqlite3 import Error

def deleteAccount(connection, accountId):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM accounts WHERE id = ?", (accountId,))
        connection.commit()
        print(f"Account with id {accountId} deleted successfully.")
    except Error as e:
        print(f"Error deleting account: {e}")