import requests

#
# Using twilio
#

ACCOUNT_SID = "ACc2d2a1cfbb454a48034bf9128d9d6a8a"
AUTH_TOKEN = "1a23dca1885b8ed1a84f1bde977e1a53"
URL_TEMPLATE = 'https://api.twilio.com/2010-04-01/Accounts/%s/Messages'


def send_sms(to, sender, message):
    data = {
        'To': to,
        'From': sender,
        'Body': message
    }
    url = URL_TEMPLATE % ACCOUNT_SID
    r = requests.post(url,data=data,verify=False)