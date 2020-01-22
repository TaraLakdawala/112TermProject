from twilio.rest import Client

acctSid=''
authToken=''

client=Client(acctSid, authToken)

def sendMessage(number, client):
    message=client.api.account.messages.create(f'+1{number}', from_='+12563636816', 
            body='It\'s almost time for your workout! Let\'s hit the gym!')

