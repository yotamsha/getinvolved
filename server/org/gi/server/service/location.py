import requests
import time
from org.gi.server import utils as u

__author__ = 'avishayb'


_API_KEY = 'AIzaSyCSDWhR_zQ-lFJuEHmBeG_Kawd2UBp8eTo'
URL_TEMPLATE = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'
REVERSE_URL_TEMPLATE = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&language=%s&key=%s'
RETRY_STATUSES = set([u.HTTP_SERVER_ERROR, u.HTTP_GATEWAY_TIMEOUT, u.HTTP_SERVICE_UNAVAILABLE])
MAX_RETRY = 5


def get_address(lat, lng, lang='iw'):
    if not lat or not lng:
        raise Exception('Lat and Lng must be specified')
    if not isinstance(lat, float):
        raise Exception('Lat must be a floating number')
    if not isinstance(lng, float):
        raise Exception('Lng must be a floating number')
    reverse_result = _get_result(REVERSE_URL_TEMPLATE % (lat, lng, lang, _API_KEY))
    if not reverse_result:
        raise Exception('Failed to get address for [%d,%d]' % (lat,lng))
    else:
        address_list = reverse_result[0]['formatted_address'].split(',')
        return {'country': address_list[2], 'city': address_list[1], 'street': address_list[0]}


def get_lat_lng(address):
    if not address:
        raise Exception('address can not be None')
    if not isinstance(address, (str, unicode, dict)):
        raise Exception('address must be a string or dict')
    if isinstance(address, dict):
        fields = ['city', 'country', 'street_name', 'street_number']
        for field in fields:
            if field not in address:
                raise Exception('The field \'%s\' is mandatory' % field)
        address = ' , '.join(address.get(field) for field in fields)
    geocode_result = _get_result(URL_TEMPLATE % (address, _API_KEY))
    if geocode_result:
        if len(geocode_result) != 1:
            raise Exception('Expecting one result but got %d results' % len(geocode_result))
        else:
            return geocode_result[0]['geometry']['location']
    else:
        raise Exception('Failed to geocode the address %s.' % address)


def _get_result(url):
    result = None
    r = requests.get(url, verify=False)
    if r.status_code != u.HTTP_OK:
        if r.status_code in RETRY_STATUSES:
            counter = 0
            status_code = -1
            while counter < MAX_RETRY and status_code != u.HTTP_OK:
                time.sleep(1)
                r = requests.get(url, verify=False)
                if r.status_code == u.HTTP_OK:
                    result = r.json()
                counter += 1
                status_code = r.status_code
        else:
            raise Exception('Failed to geocode the url %s. Status code is %d' % (url, r.status_code ))
    else:
        result = r.json()
    return result['results']