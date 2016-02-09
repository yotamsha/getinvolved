import json

from org.gi.server import utils as u
from org.gi.server import db

__author__ = 'avishayb'
import re
import phonenumbers
import pycountry
import time
import org.gi.server.authorization as auth

MANDATORY = True

WSP = r'[\s]'  # see 2.2.2. Structured Header Field Bodies
CRLF = r'(?:\r\n)'  # see 2.2.3. Long Header Fields
NO_WS_CTL = r'\x01-\x08\x0b\x0c\x0f-\x1f\x7f'  # see 3.2.1. Primitive Tokens
QUOTED_PAIR = r'(?:\\.)'  # see 3.2.2. Quoted characters
FWS = r'(?:(?:' + WSP + r'*' + CRLF + r')?' + \
      WSP + r'+)'  # see 3.2.3. Folding white space and comments
CTEXT = r'[' + NO_WS_CTL + \
        r'\x21-\x27\x2a-\x5b\x5d-\x7e]'  # see 3.2.3
CCONTENT = r'(?:' + CTEXT + r'|' + \
           QUOTED_PAIR + r')'  # see 3.2.3 (NB: The RFC includes COMMENT here
# as well, but that would be circular.)
COMMENT = r'\((?:' + FWS + r'?' + CCONTENT + \
          r')*' + FWS + r'?\)'  # see 3.2.3
CFWS = r'(?:' + FWS + r'?' + COMMENT + ')*(?:' + \
       FWS + '?' + COMMENT + '|' + FWS + ')'  # see 3.2.3
ATEXT = r'[\w!#$%&\'\*\+\-/=\?\^`\{\|\}~]'  # see 3.2.4. Atom
ATOM = CFWS + r'?' + ATEXT + r'+' + CFWS + r'?'  # see 3.2.4
DOT_ATOM_TEXT = ATEXT + r'+(?:\.' + ATEXT + r'+)*'  # see 3.2.4
DOT_ATOM = CFWS + r'?' + DOT_ATOM_TEXT + CFWS + r'?'  # see 3.2.4
QTEXT = r'[' + NO_WS_CTL + \
        r'\x21\x23-\x5b\x5d-\x7e]'  # see 3.2.5. Quoted strings
QCONTENT = r'(?:' + QTEXT + r'|' + \
           QUOTED_PAIR + r')'  # see 3.2.5
QUOTED_STRING = CFWS + r'?' + r'"(?:' + FWS + \
                r'?' + QCONTENT + r')*' + FWS + \
                r'?' + r'"' + CFWS + r'?'
LOCAL_PART = r'(?:' + DOT_ATOM + r'|' + \
             QUOTED_STRING + r')'  # see 3.4.1. Addr-spec specification
DTEXT = r'[' + NO_WS_CTL + r'\x21-\x5a\x5e-\x7e]'  # see 3.4.1
DCONTENT = r'(?:' + DTEXT + r'|' + \
           QUOTED_PAIR + r')'  # see 3.4.1
DOMAIN_LITERAL = CFWS + r'?' + r'\[' + \
                 r'(?:' + FWS + r'?' + DCONTENT + \
                 r')*' + FWS + r'?\]' + CFWS + r'?'  # see 3.4.1
DOMAIN = r'(?:' + DOT_ATOM + r'|' + \
         DOMAIN_LITERAL + r')'  # see 3.4.1
ADDR_SPEC = LOCAL_PART + r'@' + DOMAIN  # see 3.4.1

# A valid address will match exactly the 3.4.1 addr-spec.
VALID_ADDRESS_REGEXP = '^' + ADDR_SPEC + '$'


def validate_email(email, faults):
    """Indicate whether the given string is a valid email address
    according to the 'addr-spec' portion of RFC 2822 (see section
    3.4.1).  Parts of the spec that are marked obsolete are *not*
    included in this test, and certain arcane constructions that
    depend on circular definitions in the spec may not pass, but in
    general this should correctly identify any email address likely
    to be in use as of 2011."""

    try:
        assert re.match(VALID_ADDRESS_REGEXP, email) is not None
    except AssertionError:
        faults.append('%s is not a valid email address' % email)


PASSWORD_MIN = 8
PASSWORD_MAX = 12

FIRST_NAME_MIN = 2
FIRST_NAME_MAX = 22

LAST_NAME_MIN = 2
LAST_NAME_MAX = 22

USER_NAME_MIN = 2
USER_NAME_MAX = 22

TITLE_NAME_MIN = 2
TITLE_NAME_MAX = 22

DESCRIPTION_NAME_MIN = 2
DESCRIPTION_NAME_MAX = 22

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

STATES = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE',
          'FL', 'GA', 'HI', 'IA', 'ID', 'IN', 'IL', 'KS', 'KY',
          'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT',
          'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH',
          'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
          'VA', 'VT', 'WA', 'WI', 'WV', 'WY']


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


def validate_phone_number(phone_number, faults):
    if not isinstance(phone_number, dict):
        faults.append('phone_number must be a dict')
        return
    if not 'number' in phone_number.keys():
        faults.append('phone_number must contain the field \'number\'')
        return
    if not 'country_code' in phone_number.keys():
        faults.append('phone_number must contain the field \'country_code\'')
        return
    try:
        number = phonenumbers.parse(str(phone_number['number']), str(phone_number['country_code']))
        valid = phonenumbers.is_valid_number(number)
        if not valid:
            faults.append(
                'The phone number %s (country %s) is invalid.' % (phone_number['number'], phone_number['country_code']))
    except Exception as e:
        faults.append('The phone number %s (country %s) is invalid. Reason: %s' % (
            phone_number['number'], phone_number['country_code'], str(e)))


def validate_password(password, faults):
    if not password or not isinstance(password, (str, unicode)):
        faults.append('password must be none empty string')
        return
    if not _validate_len_in_range(password, PASSWORD_MIN, PASSWORD_MAX):
        faults.append('%s is not a valid password. Password length should be in the range %d - %d' % (
            password, PASSWORD_MIN, PASSWORD_MAX))


def validate_first_name(first_name, faults):
    if not first_name or not isinstance(first_name, (str, unicode)):
        faults.append('first_name must be none empty string')
        return
    if not _validate_len_in_range(first_name, FIRST_NAME_MIN, FIRST_NAME_MAX):
        faults.append('%s is not a valid first name. first name length should be in the range %d - %d' % (
            first_name, FIRST_NAME_MIN, FIRST_NAME_MAX))


def validate_last_name(last_name, faults):
    if not last_name or not isinstance(last_name, (str, unicode)):
        faults.append('last_name must be none empty string')
        return
    if not _validate_len_in_range(last_name, LAST_NAME_MIN, LAST_NAME_MAX):
        faults.append('%s is not a valid first name. first name length should be in the range %d - %d' % (
            last_name, LAST_NAME_MIN, LAST_NAME_MAX))


def validate_user_name(user_name, faults):
    if not user_name or not isinstance(user_name, (str, unicode)):
        faults.append('user_name  must be none empty string')
        return
    if not _validate_len_in_range(user_name, USER_NAME_MIN, USER_NAME_MAX):
        faults.append('%s is not a valid first name. first name length should be in the range %d - %d' % (
            user_name, USER_NAME_MIN, USER_NAME_MAX))


def validate_title(title, faults):
    if not title or not isinstance(title, (str, unicode)):
        faults.append('title  must be none empty string')
        return
    if not _validate_len_in_range(title, TITLE_NAME_MIN, TITLE_NAME_MAX):
        faults.append('%s is not a valid title. title length should be in the range %d - %d' % (
            title, TITLE_NAME_MIN, TITLE_NAME_MAX))


def validate_description(description, faults):
    if not description or not isinstance(description, (str, unicode)):
        faults.append('description  must be none empty string')
        return
    if not _validate_len_in_range(description, DESCRIPTION_NAME_MIN, DESCRIPTION_NAME_MAX):
        faults.append('%s is not a valid description. description length should be in the range %d - %d' % (
            description, DESCRIPTION_NAME_MIN, DESCRIPTION_NAME_MAX))


def validate_petitioner_id(db, petitioner_id, faults):
    if not entity_exists(db, 'users', petitioner_id):
        faults.append('There is no petitioner having the id %s' % petitioner_id)


def validate_transportation_task(task, faults):
    post_validate(task, TASK_META, faults, mandatory=True)
    if not task.get('destination_address'):
        faults.append('Transportation task must contain destination address')
    if not task.get('address'):
        faults.append('Transportation task must contain address')
    if faults:
        return
    validate_address(task['destination_address'], faults)
    validate_address(task['address'], faults)


def validate_tasks(tasks, faults, current_tasks=None):
    def _validate_task(task, faults, current_task=None):
        if not task:
            faults.append("A task can not be null")
            return
        if not isinstance(task, dict):
            faults.append("task must be a dict")
            return
        if not task.get('type'):
            faults.append('A task must contain the property \'type\'. Valid type values are %s' % str(TASK_TYPES))
            return
        if task['type'] == TASK_TYPE_PRODUCT_TRANSPORTATION:
            validate_transportation_task(task, faults)
        else:
            if not current_task:
                post_validate(task, TASK_META, faults, mandatory=True)
            else:
                _validate_status_transition(current_task['state'], task['state'], VALID_TASK_STATES, TASK_TRANSITIONS,
                                            faults)
                put_validate(task, TASK_META, faults, mandatory=False)

    if not tasks:
        faults.append('A Case must have at least one task')
        return
    if not isinstance(tasks, list):
        faults.append("tasks must be a list")
        return
    for task in tasks:
        if task.get('id'):  # is it a new task or an updated one?
            if current_tasks:
                for cur_task in current_tasks:
                    if cur_task['id'] == task['id']:
                        _validate_task(task, faults, cur_task)
                        break
        else:
            _validate_task(task, faults)


def validate_case_state(state, faults):
    if state not in VALID_CASE_STATES:
        faults.append('%s is invalid case state. Valid cases states are %s' % (state, str(VALID_CASE_STATES)))


def _validate_len_in_range(value, _min, _max):
    return value and _min <= len(value.strip()) <= _max


CASE_UNDEFINED = '__undefined__'
CASE_PENDING_APPROVAL = 'pending_approval'
CASE_PENDING_INVOLVEMENT = 'pending_involvement'
CASE_PARTIALLY_ASSIGNED = 'partially_assigned'
CASE_ASSIGNED = 'assigned'
CASE_PARTIALLY_COMPLETED = 'partially_completed'
CASE_COMPLETED = 'completed'
CASE_CANCELLED_BY_USER = 'cancelled_by_user'
CASE_CANCELLED_BY_ADMIN = 'cancelled_by_admin'
CASE_MISSING_INFO = 'missing_info'
CASE_REJECTED = 'rejected'
CASE_OVERDUE = 'overdue'

VALID_CASE_STATES = {CASE_PENDING_APPROVAL, CASE_PENDING_INVOLVEMENT, CASE_PARTIALLY_ASSIGNED, CASE_ASSIGNED,
                     CASE_PARTIALLY_COMPLETED, CASE_COMPLETED, CASE_CANCELLED_BY_USER, CASE_CANCELLED_BY_ADMIN,
                     CASE_MISSING_INFO, CASE_REJECTED, CASE_OVERDUE, CASE_UNDEFINED}

CASE_TRANSITIONS = dict()
CASE_TRANSITIONS[CASE_PENDING_APPROVAL] = {CASE_MISSING_INFO, CASE_REJECTED, CASE_OVERDUE, CASE_PENDING_APPROVAL,
                                           CASE_CANCELLED_BY_USER, CASE_CANCELLED_BY_ADMIN}
CASE_TRANSITIONS[CASE_PENDING_APPROVAL] = {CASE_MISSING_INFO, CASE_REJECTED, CASE_OVERDUE, CASE_PENDING_APPROVAL,
                                           CASE_CANCELLED_BY_USER, CASE_CANCELLED_BY_ADMIN}
CASE_TRANSITIONS[CASE_MISSING_INFO] = {CASE_PENDING_APPROVAL, CASE_OVERDUE, CASE_CANCELLED_BY_USER,
                                       CASE_CANCELLED_BY_ADMIN}
CASE_TRANSITIONS[CASE_REJECTED] = {CASE_PENDING_INVOLVEMENT, CASE_CANCELLED_BY_USER, CASE_CANCELLED_BY_ADMIN}
CASE_TRANSITIONS[CASE_PENDING_INVOLVEMENT] = {CASE_PARTIALLY_ASSIGNED, CASE_ASSIGNED, CASE_OVERDUE,
                                              CASE_CANCELLED_BY_USER, CASE_CANCELLED_BY_ADMIN}
CASE_TRANSITIONS[CASE_PARTIALLY_ASSIGNED] = {CASE_ASSIGNED, CASE_OVERDUE, CASE_CANCELLED_BY_USER,
                                             CASE_CANCELLED_BY_ADMIN}
CASE_TRANSITIONS[CASE_ASSIGNED] = {CASE_PARTIALLY_COMPLETED, CASE_COMPLETED, CASE_CANCELLED_BY_USER,
                                   CASE_CANCELLED_BY_ADMIN}
CASE_TRANSITIONS[CASE_PARTIALLY_COMPLETED] = {CASE_COMPLETED, CASE_CANCELLED_BY_USER, CASE_CANCELLED_BY_ADMIN}
CASE_TRANSITIONS[CASE_COMPLETED] = set()
CASE_TRANSITIONS[CASE_OVERDUE] = set()
CASE_TRANSITIONS[CASE_UNDEFINED] = {CASE_PENDING_APPROVAL}

TASK_UNDEFINED = '__undefined__'
TASK_PENDING = 'pending'
TASK_ASSIGNMENT_IN_PROCESS = 'assignment_in_process'
TASK_PENDING_USER_APPROVAL = 'pending_user_approval'
TASK_ASSIGNED = 'assigned'
TASK_CANCELLED = 'cancelled'
TASK_COMPLETED = 'completed'

VALID_TASK_STATES = {TASK_UNDEFINED, TASK_PENDING, TASK_ASSIGNMENT_IN_PROCESS, TASK_PENDING_USER_APPROVAL,
                     TASK_ASSIGNED, TASK_CANCELLED, TASK_COMPLETED}

TASK_TRANSITIONS = dict()
TASK_TRANSITIONS[TASK_UNDEFINED] = {TASK_PENDING}
TASK_TRANSITIONS[TASK_PENDING] = {TASK_ASSIGNMENT_IN_PROCESS, TASK_ASSIGNED, TASK_CANCELLED}
TASK_TRANSITIONS[TASK_ASSIGNMENT_IN_PROCESS] = {TASK_ASSIGNED, TASK_PENDING, TASK_PENDING_USER_APPROVAL, TASK_CANCELLED}
TASK_TRANSITIONS[TASK_PENDING_USER_APPROVAL] = {TASK_PENDING, TASK_ASSIGNED}
TASK_TRANSITIONS[TASK_ASSIGNED] = {TASK_COMPLETED, TASK_CANCELLED, TASK_PENDING}
TASK_TRANSITIONS[TASK_CANCELLED] = set()
TASK_TRANSITIONS[TASK_COMPLETED] = set()


def _validate_status_transition(current_state, new_state, valid_states, valid_transitions, faults):
    if not current_state:
        faults.append('current_state argument not found')
        return

    if not new_state:
        faults.append('new_statement argument not found')
        return

    if new_state not in valid_states:
        faults.append('%s is invalid state. Valid states are %s' % (new_state, str(valid_states)))
        return

    if current_state not in valid_states:
        faults.append('%s is invalid state. Valid states are %s' % (current_state, str(valid_states)))
        return
    if new_state not in valid_transitions[current_state]:
        faults.append('The transition from state %s to state %s in invalid. Possible values for new state are %s' % (
            current_state, new_state, str(valid_transitions[current_state])))


def validate_user_role(role, faults):
    if not role or not isinstance(role, (str, unicode)):
        faults.append('User role must be non empty string')
        return
    if role not in auth.ROLES.keys():
        faults.append("Invalid role %s. Valid roles are %s" % (role, str(auth.ROLES.keys())))


def validate_mandatory_and_present_fields(payload, meta, faults):
    FUNC = 0
    MANDATORY = 1
    if not payload or not isinstance(payload, dict):
        faults.append('payload must be none empty dict')
        return
    for key in payload.keys():
        if key not in meta.keys():
            faults.append('The field \'%s\' is invalid. Valid fields are %s' % (
                key, str(meta.keys())))
    for field_name, validation_info in meta.iteritems():
        if field_name not in payload and (isinstance(validation_info, tuple) and validation_info[MANDATORY]):
            faults.append('The field %s is a mandatory field.' % field_name)
            continue
        if field_name in payload:
            if isinstance(validation_info, tuple):
                validation_info[FUNC](payload[field_name], faults)
            else:
                validation_info(payload[field_name], faults)


def validate_address(address, faults):
    FUNC = 0
    MANDATORY = 1
    if not address or not isinstance(address, dict):
        faults.append('address must be none empty dict')
        return
    for key in address.keys():
        if key not in ADDRESS_META.keys():
            faults.append('The field \'%s\' is invalid address field. Valid address fields are %s' % (
                key, str(ADDRESS_META.keys())))
    for field_name, validation_info in ADDRESS_META.iteritems():
        if field_name not in address and validation_info[MANDATORY]:
            faults.append('The field %s is a mandatory field.' % field_name)
            continue
        if field_name in address:
            validation_info[FUNC](address[field_name], faults)


def validate_street_name(street_name, faults):
    if not street_name or not isinstance(street_name, (str, unicode)):
        faults.append('street_name  must be none empty string')
        return
    if not _validate_len_in_range(street_name, STREET_NAME_MIN, STREET_NAME_MAX):
        faults.append('%s is not a valid street_name. street_name length should be in the range %d - %d' % (
            street_name, STREET_NAME_MIN, STREET_NAME_MAX))


def validate_street_number(street_number, faults):
    if not street_number or not isinstance(street_number, (str, unicode)):
        faults.append('street_number  must be none empty string')
        return
    if not _validate_len_in_range(street_number, STREET_NUMBER_MIN, STREET_NUMBER_MAX):
        faults.append('%s is not a valid street_number. street_number length should be in the range %d - %d' % (
            street_number, STREET_NUMBER_MIN, STREET_NUMBER_MAX))


def validate_entrance(entrance, faults):
    if not entrance or not isinstance(entrance, (str, unicode)):
        faults.append('entrance  must be none empty string')
        return
    if not _validate_len_in_range(entrance, ENTRANCE_MIN, ENTRANCE_MAX):
        faults.append('%s is not a valid entrance. entrance length should be in the range %d - %d' % (
            entrance, ENTRANCE_MIN, ENTRANCE_MAX))


def validate_floor(floor, faults):
    if not floor or not isinstance(floor, (str, unicode)):
        faults.append('floor must be none empty string')
        return
    if not _validate_len_in_range(floor, FLOOR_MIN, FLOOR_MAX):
        faults.append('%s is not a valid floor. floor length should be in the range %d - %d' % (
            floor, FLOOR_MIN, FLOOR_MAX))


def validate_apartment_number(apartment_number, faults):
    if not apartment_number or not isinstance(apartment_number, (str, unicode)):
        faults.append('apartment_number must be none empty string')
        return
    if not _validate_len_in_range(apartment_number, APARTMENT_NUMBER_MIN, APARTMENT_NUMBER_MAX):
        faults.append('%s is not a valid street_name. description length should be in the range %d - %d' % (
            apartment_number, APARTMENT_NUMBER_MIN, APARTMENT_NUMBER_MAX))


def validate_zip_code(zip_code, faults):
    if not zip_code or not isinstance(zip_code, (str, unicode)):
        faults.append('zip_code must be none empty string')
        return
    if not _validate_len_in_range(zip_code, ZIP_CODE_MIN, ZIP_CODE_MIN_MAX):
        faults.append('%s is not a valid zip_code. zip_code length should be in the range %d - %d' % (
            zip_code, ZIP_CODE_MIN, ZIP_CODE_MIN_MAX))


def validate_city(city, faults):
    if not city or not isinstance(city, (str, unicode)):
        faults.append('city must be none empty string')
        return
    if not _validate_len_in_range(city, CITY_MIN, CITY_MAX):
        faults.append('%s is not a valid city. city length should be in the range %d - %d' % (
            city, CITY_MIN, CITY_MAX))


def validate_task_state(state, faults):
    if state not in VALID_TASK_STATES:
        faults.append('task state must be none empty string belongs to the set %s' % str(VALID_TASK_STATES))


def validate_task_type(task_type, faults):
    if task_type not in TASK_TYPES:
        faults.append('task_type type must be none empty string belongs to the set %s' % str(TASK_TYPES))


def noop(nada, faults):
    pass


MAX_DUE_DATE_HOURS = 24


def validate_date_in_the_future(due_date, faults):
    if not due_date or not isinstance(due_date, int):
        faults.append('due_date must be none empty int')
        return
    now = int(time.time())
    if due_date <= now or due_date >= now + MAX_DUE_DATE_HOURS * 60 * 60:
        faults.append('Invalid due date. due date can not be in the past or later than %d hours' % MAX_DUE_DATE_HOURS)


def validate_task_description(validate_task, faults):
    pass


def validate_task_title(task_title, faults):
    pass


def validate_facebook_id(facebook_id, faults):
    if not facebook_id or not (isinstance(facebook_id, str) or isinstance(facebook_id, basestring)):
        faults.append('facebook_id must be a none empty string')
        return
    if len(facebook_id) <= 8 or len(facebook_id) > 30:
        faults.append('facebook_id must be between 0-30 characters')
    if not facebook_id.isdigit():
        faults.append('facebook_id must be all digits')


def validate_facebook_access_token(fb_access_token, faults):
    if not fb_access_token or not (isinstance(fb_access_token, str) or isinstance(fb_access_token, basestring)):
        faults.append('fb_access_token must be a none empty string')
        return
    if len(fb_access_token) < 10:
        faults.append('fb_access_token must be atleast 10 characters')


USER_META = {
    'first_name': (validate_first_name, MANDATORY),
    'last_name': (validate_last_name, MANDATORY),
    'user_name': validate_user_name,
    'password': validate_password,
    'email': (validate_email, MANDATORY),
    'phone_number': validate_phone_number,
    'role': (validate_user_role, MANDATORY),
    'facebook_id': validate_facebook_id,
    'facebook_access_token': validate_facebook_access_token
}

CASE_META = {
    'title': validate_title,
    'description': validate_description,
    'petitioner_id': noop,
    'tasks': validate_tasks,
    'state': validate_case_state,
}

TASK_META = {
    'address': None,
    'destination_address': None,
    'volunteer_id': None,
    'description': validate_task_description,
    'title': validate_task_title,
    'state': validate_task_state,
    'type': validate_task_type,
    'due_date': validate_date_in_the_future,
    'created_at': None,
    'updated_at': None
}

ADDRESS_META = {
    'street_name': (validate_street_name, True),
    'street_number': (validate_street_number, True),
    'entrance': (validate_entrance, False),
    'floor': (validate_floor, False),
    'apartment_number': (validate_apartment_number, False),
    'zip_code': (validate_zip_code, False),
    'city': (validate_city, True),
    'state': (validate_state, False),
    'country': (validate_country, True)

}

TASK_TYPE_GENERAL = 'GENERAL'
TASK_TYPE_PRODUCT_REQUEST = 'PRODUCT_REQUEST'
TASK_TYPE_PRODUCT_DONATION = 'DONATION'
TASK_TYPE_PRODUCT_TRANSPORTATION = 'TRANSPORTATION'

TASK_TYPES = [TASK_TYPE_GENERAL, TASK_TYPE_PRODUCT_REQUEST, TASK_TYPE_PRODUCT_DONATION,
              TASK_TYPE_PRODUCT_TRANSPORTATION]


def entity_exists(db, collection_name, entity_id):
    try:
        entity = db[collection_name].find_one({'_id': u.to_object_id(entity_id)})
        return entity is not None
    except Exception:
        return False


def user_put_validate(user_updates, faults):
    if isinstance(user_updates, unicode):
        try:
            user_updates = json.loads(user_updates)
        except:
            faults.append('Bad entity body: {}'.format(user_updates))
            return
    if not user_updates or len(user_updates) <= 0:
        faults.append('No update fields supplied')
        return
    validate_fields(user_updates.keys(), user_updates, USER_META, faults)


def user_post_validate(user, faults):
    local = ['user_name', 'password', 'phone_number']
    fb = ['facebook_id', 'facebook_access_token']
    if not validate_fields(local, user, USER_META) and not validate_fields(fb, user, USER_META):
        faults.append('User must have atleast one of the following field groups. fb:{} local:{}'.format(fb, local))
        return
    validate_mandatory_and_present_fields(user, USER_META, faults)
    if faults:
        return


def validate_fields(fields, payload, meta, dummy_faults=None):
    if not dummy_faults:
        dummy_faults = []
    for field in fields:
        if field in payload and field in meta:
            if isinstance(meta[field], tuple):
                meta[field][0](payload[field], dummy_faults)
            else:
                meta[field](payload[field], dummy_faults)
            if dummy_faults:
                return False
        else:
            return False
    return True


def case_put_validate(current_case, updated_case, faults):
    _validate_status_transition(current_case['state'], updated_case['state'], VALID_CASE_STATES, CASE_TRANSITIONS,
                                faults)
    if faults:
        return
    else:
        if updated_case['state'] == CASE_COMPLETED and len(updated_case['tasks']) != sum(
                1 for task in updated_case['tasks'] if task['state'] == TASK_COMPLETED):
            faults.append(
                'A case cant be marked as %s until all tasks are marked as %s' % (CASE_COMPLETED, TASK_COMPLETED))


def case_post_validate(payload, db, faults):
    post_validate(payload, CASE_META, faults)
    if faults:
        return
    validate_petitioner_id(db, payload['petitioner_id'], faults)


def put_validate(payload, meta, faults):
    post_validate(payload, meta, faults, mandatory=False)


def post_validate(payload, meta, faults, mandatory=True):
    if not payload:
        faults.append("payload is empty")
        return
    if not isinstance(payload, dict):
        faults.append("payload must be a dict")
        return
    if not meta:
        faults.append("meta is empty")
        return
    if not isinstance(meta, dict):
        faults.append("meta must be a dict")
        return
    if not isinstance(faults, list):
        faults.append("faults must be a list")
        return
    for field_name in meta.keys():
        if field_name not in payload.keys() and mandatory and meta[field_name]:
            faults.append('The field \'%s\' can not be found in incoming payload' % field_name)
    for field_name in payload.keys():
        if field_name not in meta.keys():
            faults.append('The field \'%s\' in invalid field. Valid field names are: %s' % (field_name, str(meta.keys())))
    if faults:
        return
    for field_name, field_validator in meta.iteritems():
        if field_name in payload and field_validator:
            field_validator(payload[field_name], faults)

