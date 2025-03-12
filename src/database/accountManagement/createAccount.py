from sqlite3 import Error

def createAccount(connection, name, surname, username, email, password,
                  challengeId, homeId, workplaceId,
                  avatar=None, points=0, averageSpeed=20):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO accounts 
            (name, surname, username, email, password, avatar, challengeId, points, homeId, workplaceId, averageSpeed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, surname, username, email, password, avatar, challengeId, points, homeId, workplaceId, averageSpeed))
        connection.commit()
        accountId = cursor.lastrowid
        print(f"Account for '{username}' created successfully with id {accountId}.")
        return accountId
    except Error as e:
        print(f"Error creating account: {e}")
        return None