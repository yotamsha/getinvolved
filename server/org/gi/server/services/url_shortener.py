__author__ = 'avishayb'
import requests
#
# Using https://app.bitly.com
# See https://www.assembla.com/spaces/getinvolved/wiki/Short_URL_service_details for account details
#
ACCESS_TOKEN = '79b712bf24a7fa041c71b342323d537a660aaeb9'
URL_TEMPLATE = 'https://api-ssl.bitly.com/v3/shorten?access_token=%s&longUrl=%s&format=txt'


def get_short_url(long_url):
    if not long_url or not isinstance(long_url, str):
        raise Exception('long_url must be a none empty string')
    url = URL_TEMPLATE % (ACCESS_TOKEN, long_url)
    r = requests.get(url, verify=False)
    return r.status_code == 200, r.text.rstrip()

