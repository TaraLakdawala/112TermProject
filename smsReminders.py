from twilio.rest import Client

acctSid='AC1ecb7981d8e9724b2e9b3af6a0d521cb'
authToken='f0486550029d362ad256b7b03cab0c0b'

client=Client(acctSid, authToken)

def sendMessage(number, client):
    message=client.api.account.messages.create(f'+1{number}', from_='+12563636816', 
            body='It\'s almost time for your workout! Let\'s hit the gym!')

