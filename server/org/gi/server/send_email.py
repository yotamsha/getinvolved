__author__ = 'avishayb'
import requests

#
# Using mailgun
#

API_KEY = 'key-dbff3e0ffe49286ed318266c3233b07a'
DOMAIN = 'sandbox678d079fe13a4b8db1a9f3a6d3a797fb.mailgun.org'
URL_TEMPLATE = 'https://api.mailgun.net/v3/%s/messages'

def send_email(to, subject, message, sender, test_mode=False, cc=None, bcc=None):
    url = URL_TEMPLATE % DOMAIN
    data = {
        'to': to,
        'subject': subject,
        'text': message,
        'from': sender,
        'o:testmode': test_mode

    }
    r = requests.post(url, data=data, auth=('api', API_KEY), verify=False)
    return r.status_code == 200, r.json()['id']
