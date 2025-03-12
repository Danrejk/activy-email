from sqlite3 import Error

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
