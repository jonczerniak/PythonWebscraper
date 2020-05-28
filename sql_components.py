import pyodbc

class sqlWriter:
    server = '<ServerAddress>'
    database = 'EVChargingData'
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')

    def __init__(self, inputDictionary):
        self.inputDictionary = inputDictionary

    def writeToDb(self):
        # sql Database Connection strings
        cursor = sqlWriter.cnxn.cursor()

        for key, val in self.inputDictionary.items():
            location = str(key)
            urlID = str(val[0])
            rating = str(val[1])
            reviews = str(val[2])
            executeCommand = "insert into plugshare_reviews(station_name, url_ID, rating,reviews,date)values('{0}',{1},{2},{3},CURRENT_TIMESTAMP)"\
                .format(location, urlID, rating, reviews)
            cursor.execute(executeCommand)
            sqlWriter.cnxn.commit()


# new class sql reader
class sqlReader():

    def __init__(self, urlID):
        self.urlID = urlID

    # overloaded method
    def queryFromDb(self):
        # define parameters for the overload
        print(self.urlID)
        if self.urlID is not None:
            whereClause = " = {0}".format(self.urlID)
        else:
            whereClause = " != 0"

        queryResults = {}
        cursor = sqlWriter.cnxn.cursor()
        cursor.execute("SELECT station_name, url_ID, station_type FROM evse_public_list WHERE url_ID {0}" .format(whereClause))
        # place query result in a variable. Return variable
        for row in cursor.fetchall():
            queryResults.update({row[0] : row[1]})
        return queryResults

class sqlUpdater():

    def __init__(self):
        pass

    def changeUrlId(self, currentUrlId, newUrlId):
        idResult = ""
        cursor = sqlWriter.cnxn.cursor()
        # query db to get id to update the desired record
        cursor.execute("SELECT id, station_name FROM evse_public_list WHERE url_ID = {0}".format(currentUrlId))
        for row in cursor.fetchall():
            idResult = str(row[0])

        try:
            cursor.execute(" UPDATE evse_public_list SET url_ID = {0} WHERE id = {1}".format(newUrlId, idResult))
            cursor.commit()
        except:
            print("Update was unable to process")



