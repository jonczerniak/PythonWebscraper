from bs4 import BeautifulSoup
import requests
import re
from datetime import date
import csv
# import local classes
from emailSender import EmailSender
from sql_components import sqlWriter
from sql_components import sqlReader



# Methods ---------------------------------------------------------
# import csv with previous scrapes.  If no csv is available then create one
def importPreviousCsv(scrapeFile):
    # dictionary variable to hold csv contents
    scrapeDict = {}
    try:
        print('opening file {0}'.format(scrapeFile))
        with open(scrapeFile,'r') as csvfile:
            file_reader = csv.reader(csvfile)
            index = 1
            for row in file_reader:
                scrapeDict[index] = row
                index += 1
            print("exporting dictionary\n")
            return scrapeDict
    except:
        print("no file exists. creating file")
        with open(scrapeFile, 'w') as csvfile:
            csvfile.write('')
            print('file created\n')
            return scrapeDict



def scrapeRatings(urlLocation, urlID):
    print("checking location {0} with ID {1}".format(urlLocation, urlID))

    URL = 'https://www.plugshare.com/location/{0}'.format(urlID)


    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    soupText = str(soup)

    # regex to find the ratings within the soup
    ratingValue = re.search(r'\"ratingValue":\s"\d+\.\d"', soupText)
    reviewCount = re.search(r'"reviewCount":\s"\d+"', soupText)

    try:
        # parse results into a string values
        ratingValueSplit = (ratingValue.group(0)).split()
        ratingValueValue = float(str(ratingValueSplit[1]).replace('"', ''))

        # if the URL no longer works it will fail here
        try:
            reviewCountSplit = (reviewCount.group(0)).split()
            reviewCountValue = int(str(reviewCountSplit[1]).replace('"', ''))
        except:
            print("something is off.  Send an email to alert something went wrong")
            emailObj = EmailSender(urlLocation, urlID, "", False)
            emailObj.notifyOfChange()

        # append all values into a 1 dimensional array
        soupResults = {urlLocation: [urlID, ratingValueValue, reviewCountValue]}
    except:
        soupResults = {urlLocation: [urlID, 0, 0]}
        print("failed: here is what is being committed {0}".format(soupResults))

    return soupResults

def compareScrapes(previousScrapeDict, currentScrapeDict):
    # loop through the report array to populate the previous scrape dictionary
    ratingChanged = False
    fullMessage = []
    for key, value in previousScrapeDict.items():
        # convert value into a literal string
        previousValue = str(value[1]).strip()
        # loop through current scrape and compare the results
        for currentKey, currentValue in currentScrapeDict.items():

            # convert currentKey into a string value
            currentKey = str(currentKey).strip()
            if previousValue == currentKey:
                if int(value[4]) != int(currentValue[2]):
                    fullMessage.append("New ratings for station: {0}".format(currentKey))
                    fullMessage.append("{0} ratings increased to {1} ratings".format(value[4], currentValue[2]))
                    fullMessage.append("URL: https://www.plugshare.com/location/{0}\n".format(str(currentValue[0])))
                    ratingChanged = True
                else:
                    print("{0}: No changes to the ratings since last check\n".format(previousValue))

    # if rating changed is true call emailSender
    if ratingChanged == True:
        sender = EmailSender(currentScrapeDict.keys(), currentScrapeDict.values(),fullMessage, True)
        sender.notifyOfChange()

    return fullMessage

def writeToFile(dictionary, scrapeFile, writeType):
    # if appending also write to Db
    if writeType == 'a':
        sqlData = sqlWriter(dictionary)
        sqlData.writeToDb()

    # write to flat-files
    with open(scrapeFile, writeType) as csvfile:
        for key, value in dictionary.items():
            keyString = str(key).replace("'", "")
            valueString = str(value).replace("[", "").replace("]", "")
            row_string = str("{0}, {1}, {2}".format((str(today)), keyString, valueString))
            csvfile.write(row_string + '\n')


# END Methods --------------------------------------------------------------


currentScrapeDict = {}
today = date.today()
previousScrapeDict = importPreviousCsv('previousScrape.csv')
archiveScrapeDict = importPreviousCsv('archiveScrape.csv')
# query EVSE from the database
evseLocation = sqlReader(None)

for key, value in evseLocation.queryFromDb().items():
    # check for 0 value url_IDs
    currentScrapeDict.update(scrapeRatings(key, value))

# check the previousScrape dictionary to see if this is the first time running the program
if len(previousScrapeDict) == 0:
    # commit new dictionary to the csv file.  Save file.
    writeToFile(currentScrapeDict, 'previousScrape.csv', 'w')
else:
    #run comparison and overwrite previous results
    compareResults = compareScrapes(previousScrapeDict, currentScrapeDict)
    for ind in compareResults:
        print(ind)
    writeToFile(currentScrapeDict, 'previousScrape.csv', 'w')

#check to see if this is the first time running the program. It true write results to archive
if len(archiveScrapeDict) == 0:
    writeToFile(currentScrapeDict, 'archiveScrape.csv', 'w')
else:
    #run comparison and update results
    writeToFile(currentScrapeDict, 'archiveScrape.csv', 'a')


print('\nprevious scrape and archive scrape files have been updated')

