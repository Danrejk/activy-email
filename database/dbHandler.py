import sqlite3
from sqlite3 import Error
from placeManagement import createPlace, getPlaceById, isWorkplace, getAllWorkplaces, getAllNonWorkplaces, updatePlace, deletePlace
from challengeManagement import createChallenge, getChallengeById, getAllChallenges, updateChallenge, deleteChallenge
from accountManagement import createAccount, getAccountById, getAllAccounts, updateAccount, deleteAccount

class dbHandler:
    '''
    DB Manager
    '''
    def __init__(self, dbName):
        self.dbName = dbName
        self.connection = None
        self.createConnection()

    def createConnection(self):
        try:
            self.connection = sqlite3.connect(self.dbName)
            print(f"Connected to {self.dbName}")
        except Error as e:
            print(f"Error connecting to database: {e}")

    def closeConnection(self):
        if self.connection:
            self.connection.close()
            print(f"Connection to {self.dbName} closed.")

    def createTables(self):
        try:
            cursor = self.connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS places (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    workplace BOOLEAN NOT NULL DEFAULT FALSE
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS challenges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    startDate TIMESTAMP,
                    endDate TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    surname TEXT NOT NULL,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    avatar BLOB,
                    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    challengeId INTEGER NOT NULL,
                    points INTEGER NOT NULL DEFAULT 0,
                    homeId INTEGER NOT NULL,
                    workplaceId INTEGER NOT NULL,
                    averageSpeed REAL NOT NULL DEFAULT 20,
                    FOREIGN KEY (challengeId) REFERENCES challenges (id),
                    FOREIGN KEY (homeId) REFERENCES places (id),
                    FOREIGN KEY (workplaceId) REFERENCES places (id)
                )
            """)

            self.connection.commit()
            print("Tables 'accounts', 'places' & 'challenges' created or already exist.")
        except Error as e:
            print(f"Error creating tables: {e}")

    '''
    Place Management
    '''
    def createPlace(self, name, latitude, longitude, workplace=False):
        return createPlace(self.connection, name, latitude, longitude, workplace)

    def getPlaceById(self, placeId):
        return getPlaceById(self.connection, placeId)

    def isWorkplace(self, placeId):
        return isWorkplace(self.connection, placeId)

    def getAllWorkplaces(self):
        return getAllWorkplaces(self.connection)

    def getAllNonWorkplaces(self):
        return getAllNonWorkplaces(self.connection)

    def updatePlace(self, placeId, newName=None, newLatitude=None, newLongitude=None, newWorkplace=None):
        return updatePlace(self.connection, placeId, newName, newLatitude, newLongitude, newWorkplace)

    def deletePlace(self, placeId):
        return deletePlace(self.connection, placeId)

    '''
    Account Management
    '''
    def createAccount(self, name, surname, username, email, password, challengeId, homeId, workplaceId, avatar=None,
                      points=0, averageSpeed=20):
        return createAccount(self.connection, name, surname, username, email, password, challengeId, homeId,
                             workplaceId, avatar, points, averageSpeed)

    def getAccountById(self, accountId):
        return getAccountById(self.connection, accountId)

    def getAllAccounts(self):
        return getAllAccounts(self.connection)

    def updateAccount(self, accountId, newName=None, newSurname=None, newUsername=None, newEmail=None, newPassword=None,
                      newAvatar=None, newHomeId=None, newWorkplaceId=None, newAverageSpeed=None, newPoints=None,
                      newChallengeName=None):
        return updateAccount(self.connection, accountId, newName, newSurname, newUsername, newEmail, newPassword,
                             newAvatar, newHomeId, newWorkplaceId, newAverageSpeed, newPoints, newChallengeName)

    def deleteAccount(self, accountId):
        return deleteAccount(self.connection, accountId)

    '''
       Challenge Management
    '''
    def createChallenge(self, name, startDate=None, endDate=None):
        return createChallenge(self.connection, name, startDate, endDate)

    def getChallengeById(self, challengeId):
        return getChallengeById(self.connection, challengeId)

    def getAllChallenges(self):
        return getAllChallenges(self.connection)

    def updateChallenge(self, challengeId, newName=None, newStartDate=None, newEndDate=None):
        return updateChallenge(self.connection, challengeId, newName, newStartDate, newEndDate)

    def deleteChallenge(self, challengeId):
        return deleteChallenge(self.connection, challengeId)