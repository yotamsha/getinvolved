import requests
from requests.auth import HTTPBasicAuth
import json

#
# Using plivo
#
PLIVO_AUTH_ID = 'MANZNHZWRIYWZKYMM1ZW'
PLIVO_AUTH_TOKEN = 'OWQ3NzA0NDQ5YzA0YTg4MzU3NzUyZTQzNjA2ODUy'
PLIVO_URL_TEMPLATE = 'https://api.plivo.com/v1/Account/%s/Message/'


def send_sms(to, sender, message):
    if not to or not isinstance(to, (basestring, list)):
        raise Exception('\'to\' must be a none empty string or a list of strings')
    if not sender or not isinstance(sender, basestring):
        raise Exception('\'sender\' must be a none empty string')
    if not message or not isinstance(message, basestring):
        raise Exception('\'message\' must be a none empty string')
    if isinstance(to, list):
        to = '<'.join(to)
    data = {
        'src': sender,
        'dst': to,
        'text': message
    }
    r = requests.post(PLIVO_URL_TEMPLATE % PLIVO_AUTH_ID, data=json.dumps(data),
                      headers={'Content-type': 'application/json'}, verify=False,
                      auth=HTTPBasicAuth(PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN))
    return r.status_code == 202, r.json()

