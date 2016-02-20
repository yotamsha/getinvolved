import pycountry

from org.gi.server.validation.validation_utils import validate_len_in_range, validate_mandatory_and_present_fields

MANDATORY = True


def validate_location(location, faults):
    if location.get('address'):
        if location.get('geo_location'):
            faults.append('Location should only one ADDRESS or GEO_LOCATION')
        validate_address(location.get('address'), faults)
    elif location.get('geo_location'):
        validate_geo_location(location.get('geo_location'), faults)


def validate_geo_location(geo_location, faults):
    raise Exception('validate_geo_location not implemented')


def validate_street_name(street_name, faults):
    if not street_name or not isinstance(street_name, (str, unicode)):
        faults.append('street_name  must be none empty string')
        return
    if not validate_len_in_range(street_name, STREET_NAME_MIN, STREET_NAME_MAX):
        faults.append('%s is not a valid street_name. street_name length should be in the range %d - %d' % (
            street_name, STREET_NAME_MIN, STREET_NAME_MAX))


def validate_street_number(street_number, faults):
    if not street_number or not isinstance(street_number, (str, unicode)):
        faults.append('street_number  must be none empty string')
        return
    if not validate_len_in_range(street_number, STREET_NUMBER_MIN, STREET_NUMBER_MAX):
        faults.append('%s is not a valid street_number. street_number length should be in the range %d - %d' % (
            street_number, STREET_NUMBER_MIN, STREET_NUMBER_MAX))


def validate_entrance(entrance, faults):
    if not entrance or not isinstance(entrance, (str, unicode)):
        faults.append('entrance  must be none empty string')
        return
    if not validate_len_in_range(entrance, ENTRANCE_MIN, ENTRANCE_MAX):
        faults.append('%s is not a valid entrance. entrance length should be in the range %d - %d' % (
            entrance, ENTRANCE_MIN, ENTRANCE_MAX))


def validate_floor(floor, faults):
    if not floor or not isinstance(floor, (str, unicode)):
        faults.append('floor must be none empty string')
        return
    if not validate_len_in_range(floor, FLOOR_MIN, FLOOR_MAX):
        faults.append('%s is not a valid floor. floor length should be in the range %d - %d' % (
            floor, FLOOR_MIN, FLOOR_MAX))


def validate_apartment_number(apartment_number, faults):
    if not apartment_number or not isinstance(apartment_number, (str, unicode)):
        faults.append('apartment_number must be none empty string')
        return
    if not validate_len_in_range(apartment_number, APARTMENT_NUMBER_MIN, APARTMENT_NUMBER_MAX):
        faults.append('%s is not a valid street_name. description length should be in the range %d - %d' % (
            apartment_number, APARTMENT_NUMBER_MIN, APARTMENT_NUMBER_MAX))


def validate_zip_code(zip_code, faults):
    if not zip_code or not isinstance(zip_code, (str, unicode)):
        faults.append('zip_code must be none empty string')
        return
    if not validate_len_in_range(zip_code, ZIP_CODE_MIN, ZIP_CODE_MIN_MAX):
        faults.append('%s is not a valid zip_code. zip_code length should be in the range %d - %d' % (
            zip_code, ZIP_CODE_MIN, ZIP_CODE_MIN_MAX))


def validate_city(city, faults):
    if not city or not isinstance(city, (str, unicode)):
        faults.append('city must be none empty string')
        return
    if not validate_len_in_range(city, CITY_MIN, CITY_MAX):
        faults.append('%s is not a valid city. city length should be in the range %d - %d' % (
            city, CITY_MIN, CITY_MAX))


def validate_state(state, faults):
    if not state or not isinstance(state, (str, unicode)):
        faults.append('state must be none empty string')
        return
    if state not in STATES:
        faults.append('%s is invalid 2 chars state code.')


def validate_country(country, faults):
    if not country or not isinstance(country, (str, unicode)):
        faults.append('country must be none empty string')
        return
    try:
        pycountry.countries.get(alpha2=country)
    except KeyError, e:
        faults.append('%s is not a valid country name' % country)


def validate_address(address, faults):
    validate_mandatory_and_present_fields(address, ADDRESS_META, faults)

LOCATION_META = {
    'geo_location': validate_geo_location,
    'address': validate_address
}

# todo: Change its validation to 'validate_mandatory_and_present_fields' method
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

STREET_NAME_MIN = 3
STREET_NAME_MAX = 25

STREET_NUMBER_MIN = 1
STREET_NUMBER_MAX = 6

ENTRANCE_MIN = 1
ENTRANCE_MAX = 4

FLOOR_MIN = 1
FLOOR_MAX = 4

APARTMENT_NUMBER_MIN = 1
APARTMENT_NUMBER_MAX = 5

ZIP_CODE_MIN = 3
ZIP_CODE_MIN_MAX = 7

CITY_MIN = 3
CITY_MAX = 25
