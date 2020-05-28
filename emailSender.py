from datetime import date
from exchangelib import Credentials, Account, Message, DELEGATE


class EmailSender:
    # Initialize the class structure
    def __init__(self, stationNames, urlID, updateMessage, passFail):
        # Initialize class variables
        self.stationNames = stationNames
        self. urlID = urlID
        self.updateMessage = updateMessage
        self.passFail: bool = passFail


    def notifyOfChange(self):
        # format message body into something useful
        messageGreeting = ''
        today = str(date.today())
        # check to see if the application was a pass or a fail
        if self.passFail == True:
            messageGreeting = "Below are the stations that have received new check-ins: \n"
            formattedMessage = ''
            for ind in self.updateMessage:
                formattedMessage += str(ind + '\n')
        else:
            messageGreeting = "Station: The following station was unable to scrape.  Please check the URL " \
                              "for any discrepencies: \n"
            formattedMessage = "Station {0},\n URL https://www.plugshare.com/location/{1}".format(self.stationNames, self.urlID)

        # set exchange credentials
        credentials = Credentials('<UserName>', '<Password>')



        account = Account("<Outlook Email Address>", credentials=credentials,
                      autodiscover=True, access_type=DELEGATE)


        recipients = ['<Email Addresses>']

        #create message
        testMessage = Message(account=account,
                              folder=account.sent,
                              subject='{0} Plugshare Report (auto-generated)'.format(today),
                              body= "{0}{1}".format(messageGreeting, formattedMessage),
                              to_recipients=recipients)

        testMessage.send_and_save()
