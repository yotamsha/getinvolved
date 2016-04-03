import pycountry

from org.gi.server.validation.validation_utils import validate_len_in_range, validate_mandatory_and_present_fields, \
    get_max_len, get_min_len, LEN_ERR_MSG_TEMPLATE


def validate_location(location, faults):
    if location.get('address'):
        if location.get('geo_location'):
            faults.append('Location should have only one value: ADDRESS or GEO_LOCATION')
        validate_address(location.get('address'), faults)
    elif location.get('geo_location'):
        validate_geo_location(location.get('geo_location'), faults)


def validate_geo_location(geo_location, faults):
    lat = geo_location.get('lat')
    lng = geo_location.get('lng')
    if not (lat and lng):
        faults.append('geo_location requires both lng & lat')
    if not (isinstance(lat, float) and isinstance(lng, float)):
        faults.append('lng & lat must both be floating point numbers')
    if not (MIN_LATITUDE <= lat <= MAX_LATITUDE):
        faults.append('{} <= lat <= {}'.format(MIN_LATITUDE, MAX_LATITUDE))
    if not (MIN_LONGITUDE <= lng <= MAX_LONGITUDE):
        faults.append('{} <= lng <= {}'.format(MIN_LONGITUDE, MAX_LONGITUDE))


def validate_street_name(street_name, faults):
    if not validate_len_in_range('address', 'street_name', street_name):
        faults.append(LEN_ERR_MSG_TEMPLATE % (
            street_name, 'street_name', 'street_name', get_min_len('address', 'street_name'),
            get_max_len('address', 'street_name')))


def validate_street_number(street_number, faults):
    if not validate_len_in_range('address', 'street_number', street_number):
        faults.append(LEN_ERR_MSG_TEMPLATE % (
            street_number, 'street_number', 'street_number', get_min_len('address', 'street_number'),
            get_max_len('address', 'street_number')))


def validate_entrance(entrance, faults):
    if not validate_len_in_range('address', 'entrance', entrance):
        faults.append(LEN_ERR_MSG_TEMPLATE % (
            entrance, 'entrance', 'entrance', get_min_len('address', 'entrance'),
            get_max_len('address', 'entrance')))


def validate_floor(floor, faults):
    if not validate_len_in_range('address', 'floor', floor):
        faults.append(LEN_ERR_MSG_TEMPLATE % (
            floor, 'floor', 'floor', get_min_len('address', 'floor'), get_max_len('address', 'floor')))


def validate_apartment_number(apartment_number, faults):
    if not validate_len_in_range('address', 'apartment_number', apartment_number):
        faults.append(
            LEN_ERR_MSG_TEMPLATE % (
                apartment_number,'apartment_number', 'apartment_number', get_min_len('address', 'apartment_number'),
                get_max_len('address', 'apartment_number')))


def validate_zip_code(zip_code, faults):
    if not validate_len_in_range('address', 'zip_code', zip_code):
        faults.append(LEN_ERR_MSG_TEMPLATE% (
            zip_code,'zipcode','zipcode', get_min_len('address', 'zip_code'), get_max_len('address', 'zip_code')))


def validate_city(city, faults):
    if not validate_len_in_range('address', 'city', city):
        faults.append(LEN_ERR_MSG_TEMPLATE % (
            city,'city','city', get_min_len('address', 'city'), get_max_len('address', 'city')))


def validate_state(state, faults):
    if not state or not isinstance(state, basestring):
        faults.append('state must be none empty string')
        return
    if state not in STATES:
        faults.append('%s is invalid 2 chars state code.')


def validate_country(country, faults):
    if not country or not isinstance(country, basestring):
        faults.append('country must be none empty string')
        return
    try:
        pycountry.countries.get(alpha2=country)
    except KeyError, e:
        faults.append('%s is not a valid country name' % country)


def validate_address(address, faults):
    validate_mandatory_and_present_fields(address, ADDRESS_META, faults)


MANDATORY = True
LOCATION_META = {
    'geo_location': validate_geo_location,
    'address': validate_address
}

ADDRESS_META = {
    'street_name': (validate_street_name, MANDATORY),
    'street_number': (validate_street_number, MANDATORY),
    'entrance': (validate_entrance, not MANDATORY),
    'floor': (validate_floor, not MANDATORY),
    'apartment_number': (validate_apartment_number, not MANDATORY),
    'zip_code': (validate_zip_code, not MANDATORY),
    'city': (validate_city, MANDATORY),
    'state': (validate_state, not MANDATORY),
    'country': (validate_country, not MANDATORY),
}

STATES = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE',
          'FL', 'GA', 'HI', 'IA', 'ID', 'IN', 'IL', 'KS', 'KY',
          'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT',
          'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH',
          'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
          'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

MAX_LATITUDE = 90
MIN_LATITUDE = -90

MAX_LONGITUDE = 180
MIN_LONGITUDE = -180
