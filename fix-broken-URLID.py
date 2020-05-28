# imports
import sys
from sql_components import sqlReader
from sql_components import sqlUpdater

# methods
def inputAuthentication(userInput):
    urlLocationID = 0
    if userInput.isnumeric() == False:
        correctInputType = False
        while correctInputType == False:
            userInput = input("Please enter only the 5-6 digit number following 'location/' in the URL: ")
            # convert string to text.  If it fails prompt user to try again
            try:
                urlLocationID = int(userInput)
            except:
                pass
            if (urlLocationID):
                correctInputType = True
                print("URL meets criteria")
                return urlLocationID
    else:
        return userInput





# provide user a prompt and ask for input
brokenURL = input("Please enter the 5-6 digit URL location ID that is not working: ")
# authenticate url
searchURL = inputAuthentication(brokenURL)


# create sql_component object then query the database
# try catch block
print("Before the query, this is the value being used: {0}".format(searchURL))
getUrlId = sqlReader(searchURL).queryFromDb()

# check for results
if len(getUrlId) == 0:
    print("ID did not return any results.")
    tryCounter = 0
    returnResults = False
    while returnResults == False:
        if tryCounter == 3:
            print("Unable to find the ID.  Please go back and check your ID, or utilize the Database method referenced"
                  "the documentation.")
            sys.exit()
        else:
            searchURL = input("Unable to find ID.  Please enter the 5-6 digit URL location ID that is not working: ")
            inputAuthentication(searchURL)
            getUrlId = sqlReader(searchURL).queryFromDb()
            if len(getUrlId) > 0:

                returnResults = True
            else:
                tryCounter += 1


print("Here are the results of the query:")
print(getUrlId)

continueToUpdate = input("Is this the correct record? (Y/N) ")
continueToUpdate = continueToUpdate.upper()

if (continueToUpdate != "N" and continueToUpdate != "n") and (continueToUpdate != "Y" and continueToUpdate != 'y'):
    correctInput = False
    while correctInput == False:
        continueToUpdate = input("Please enter Y or N: ")
        continueToUpdate = continueToUpdate.upper()
        if continueToUpdate.upper() == "Y" or continueToUpdate == "N":
            print('input accepted')
            correctInput = True


# check to see if user wants to continue or needs to re-enter the broken ID
if continueToUpdate == "N":
    tryCounter = 0
    while continueToUpdate == "N":
        if tryCounter == 0:
            brokenURL = input("Please enter the correct urlID")
            searchURL = inputAuthentication(brokenURL)
            tryCounter += 1
        elif tryCounter == 3:
            print("Unable to find the ID.  Please go back and check your ID, or utilize the Database method referenced"
                  " the documentation.")
            sys.exit()
        else:
            searchURL = input("Unable to find ID.  Please enter the 5-6 digit URL location ID that is not working: ")
            inputAuthentication(searchURL)
            getUrlId = sqlReader(searchURL).queryFromDb()
            if len(getUrlId) > 0:
                print("Here are the results of the query:")
                print(getUrlId)
                continueToUpdate = "Y"
            else:
                tryCounter += 1


# return the results and ask user for new ID
newUrlID = input("Please input the new ID for this Station: ")
updateRecord = False
inputAuthentication(newUrlID)
confirmationInput = input("You entered {0}. Are you sure you want to update to this ID? (Y/N)".format(newUrlID))
confirmationInput.upper()
if confirmationInput == 'Y' or confirmationInput == 'y':
    updateRecord = True
else:
    while updateRecord == False:
        newUrlID = input("Please input the new ID for this Station: ")
        confirmationInput = input("You entered {0}. Are you sure you want to update to this ID? (Y/N)".format(newUrlID))
        confirmationInput.upper()

        if confirmationInput == 'Y' or confirmationInput == 'y':
            updateRecord = True

print("Updating record {0} to {1}...".format(brokenURL, newUrlID))

updateQuery = sqlUpdater()
updatedResults = updateQuery.changeUrlId(brokenURL, newUrlID)
print("Records Updated")




