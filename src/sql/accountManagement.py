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
        """, (name, surname, username, email, password, avatar, homeId, workplaceId, averageSpeed, points, challengeId))
        connection.commit()
        accountId = cursor.lastrowid
        print(f"Account for '{username}' created successfully with id {accountId}.")
        return accountId
    except Error as e:
        print(f"Error creating account: {e}")
        return None

def getAccountById(connection, accountId):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM accounts WHERE id = ?", (accountId,))
        account = cursor.fetchone()
        if account:
            print(f"Account found: {account}")
        else:
            print(f"No account found with id: {accountId}")
        return account
    except Error as e:
        print(f"Error fetching account by id: {e}")
        return None

def getAllAccounts(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM accounts")
        accounts = cursor.fetchall()
        if accounts:
            print(f"Fetched {len(accounts)} account(s).")
        else:
            print("No accounts found.")
        return accounts
    except Error as e:
        print(f"Error fetching accounts: {e}")
        return []

def deleteAccount(connection, accountId):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM accounts WHERE id = ?", (accountId,))
        connection.commit()
        print(f"Account with id {accountId} deleted successfully.")
    except Error as e:
        print(f"Error deleting account: {e}")

def updateAccount(connection, accountId, newName=None, newSurname=None, newUsername=None,
                  newEmail=None, newPassword=None, newAvatar=None, newHomeId=None,
                  newWorkplaceId=None, newAverageSpeed=None, newPoints=None, newChallengeName=None):
    try:
        cursor = connection.cursor()
        updates = []
        params = []

        if newName is not None:
            updates.append("name = ?")
            params.append(newName)
        if newSurname is not None:
            updates.append("surname = ?")
            params.append(newSurname)
        if newUsername is not None:
            updates.append("username = ?")
            params.append(newUsername)
        if newEmail is not None:
            updates.append("email = ?")
            params.append(newEmail)
        if newPassword is not None:
            updates.append("password = ?")
            params.append(newPassword)
        if newAvatar is not None:
            updates.append("avatar = ?")
            params.append(newAvatar)
        if newChallengeName is not None:
            updates.append("challengeName = ?")
            params.append(newChallengeName)
        if newPoints is not None:
            updates.append("points = ?")
            params.append(newPoints)
        if newHomeId is not None:
            updates.append("homeId = ?")
            params.append(newHomeId)
        if newWorkplaceId is not None:
            updates.append("workplaceId = ?")
            params.append(newWorkplaceId)
        if newAverageSpeed is not None:
            updates.append("averageSpeed = ?")
            params.append(newAverageSpeed)

        if not updates:
            print("No update parameters provided; nothing to change.")
            return

        query = f"UPDATE accounts SET {', '.join(updates)} WHERE id = ?"
        params.append(accountId)
        cursor.execute(query, tuple(params))
        connection.commit()
        print(f"Account with id {accountId} updated successfully.")
    except Error as e:
        print(f"Error updating account: {e}")
