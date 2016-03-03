import json
import re
import time

import phonenumbers

import org.gi.server.authorization as auth
import org.gi.server.validation.location_validator as location_validator
from org.gi.server import utils as u
from org.gi.server.db import db
from org.gi.server.validation.case_state_machine import VALID_CASE_STATES, CASE_COMPLETED, CASE_TRANSITIONS
from org.gi.server.validation.task import TASK_TYPES, TASK_TYPE_PRODUCT_TRANSPORTATION
from org.gi.server.validation.task.task_state_machine import VALID_TASK_STATES, TASK_COMPLETED, TASK_TRANSITIONS
from org.gi.server.validation.validation_utils import validate_len_in_range, validate_mandatory_and_present_fields

__author__ = 'avishayb'

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

FB_TOKEN_MIN_LENGTH = 10
FB_ID_MIN_LENGTH = 8
FB_ID_MAX_LENGTH = 40

MAX_DUE_DATE_HOURS = 24

TASK_MIN_DURATION_MINUTES = 60
TASK_MAX_DURATION_MINUTES = 60 * 24

ONE_DAY_SECONDS = 60 * 60 * 24
MIN_DUE_DATE_SECONDS = ONE_DAY_SECONDS
MAX_DUE_DATE_SECONDS = ONE_DAY_SECONDS * 90

TASK_DESCRIPTION_MIN = 10
TASK_DESCRIPTION_MAX = 50

TASK_TITLE_MIN = 8
TASK_TITLE_MAX = 25


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
    if not validate_len_in_range(password, PASSWORD_MIN, PASSWORD_MAX):
        faults.append('%s is not a valid password. Password length should be in the range %d - %d' % (
            password, PASSWORD_MIN, PASSWORD_MAX))


def validate_first_name(first_name, faults):
    if not first_name or not isinstance(first_name, (str, unicode)):
        faults.append('first_name must be none empty string')
        return
    if not validate_len_in_range(first_name, FIRST_NAME_MIN, FIRST_NAME_MAX):
        faults.append('%s is not a valid first name. first name length should be in the range %d - %d' % (
            first_name, FIRST_NAME_MIN, FIRST_NAME_MAX))


def validate_last_name(last_name, faults):
    if not last_name or not isinstance(last_name, (str, unicode)):
        faults.append('last_name must be none empty string')
        return
    if not validate_len_in_range(last_name, LAST_NAME_MIN, LAST_NAME_MAX):
        faults.append('%s is not a valid first name. first name length should be in the range %d - %d' % (
            last_name, LAST_NAME_MIN, LAST_NAME_MAX))


def validate_user_name(user_name, faults):
    if not user_name or not isinstance(user_name, (str, unicode)):
        faults.append('user_name  must be none empty string')
        return
    if not validate_len_in_range(user_name, USER_NAME_MIN, USER_NAME_MAX):
        faults.append('%s is not a valid first name. first name length should be in the range %d - %d' % (
            user_name, USER_NAME_MIN, USER_NAME_MAX))


def validate_title(title, faults):
    if not title or not isinstance(title, (str, unicode)):
        faults.append('title  must be none empty string')
        return
    if not validate_len_in_range(title, TITLE_NAME_MIN, TITLE_NAME_MAX):
        faults.append('%s is not a valid title. title length should be in the range %d - %d' % (
            title, TITLE_NAME_MIN, TITLE_NAME_MAX))


def validate_description(description, faults):
    if not description or not isinstance(description, (str, unicode)):
        faults.append('description  must be none empty string')
        return
    if not validate_len_in_range(description, DESCRIPTION_NAME_MIN, DESCRIPTION_NAME_MAX):
        faults.append('%s is not a valid description. description length should be in the range %d - %d' % (
            description, DESCRIPTION_NAME_MIN, DESCRIPTION_NAME_MAX))


def validate_petitioner_id(petitioner_id, faults):
    if not entity_exists('users', petitioner_id):
        faults.append('There is no petitioner having the id %s' % petitioner_id)


def validate_transportation_task(task, faults):
    validate_mandatory_and_present_fields(task, TASK_META, faults)
    if not task.get('location'):
        faults.append('Transportation task must contain location')
    if not task.get('destination'):
        faults.append('Transportation task must contain destination')
    if faults:
        return
    location_validator.validate_location(task['location'], faults)
    location_validator.validate_location(task['destination'], faults)


def validate_tasks(tasks, faults, current_tasks=None):
    def _valid_task_duration(task):
        duration = task.get('duration')
        if not duration or not isinstance(duration, int):
            return False
        if duration >= TASK_MAX_DURATION_MINUTES or duration <= TASK_MIN_DURATION_MINUTES:
            return False
        return True

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
        if task.get('state') == TASK_COMPLETED and not _valid_task_duration(task):
            faults.append(
                'In order to complete a Task an integer \'duration\' field should be passed. Valid values are in the range %d - %d' % (
                    TASK_MIN_DURATION_MINUTES, TASK_MAX_DURATION_MINUTES))
            return

        if task['type'] == TASK_TYPE_PRODUCT_TRANSPORTATION:
            validate_transportation_task(task, faults)
        else:
            if not current_task:
                validate_mandatory_and_present_fields(task, TASK_META, faults)
                # post_validate(task, TASK_META, faults, mandatory=True)
            else:
                _validate_status_transition(current_task['state'], task['state'], VALID_TASK_STATES, TASK_TRANSITIONS,
                                            faults)
                validate_mandatory_and_present_fields(task, TASK_META, faults, mandatory=True)

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
                        _validate_task(task, faults, current_task=cur_task)
                        break
        else:
            _validate_task(task, faults)


def validate_case_state(state, faults):
    if state not in VALID_CASE_STATES:
        faults.append('%s is invalid case state. Valid cases states are %s' % (state, str(VALID_CASE_STATES)))


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


def validate_task_state(state, faults):
    if state not in VALID_TASK_STATES:
        faults.append('task state must be none empty string belongs to the set %s' % str(VALID_TASK_STATES))


def validate_task_type(task_type, faults):
    if task_type not in TASK_TYPES:
        faults.append('task_type type must be none empty string belongs to the set %s' % str(TASK_TYPES))


def validate_sms_notification(sms_val, faults):
    if not validate_boolean(sms_val):
        faults.append('sms notification field must have boolean value. current value is %s' % sms_val)


def validate_email_notification(email_val, faults):
    if not validate_boolean(email_val):
        faults.append('email notification field must have boolean value. current value is %s' % email_val)


def validate_boolean(val):
    return val is not None and isinstance(val, bool)


def noop(nada, faults):
    pass


def validate_task_id(task_id, faults):
    pass


def validate_notifications(notification, faults):
    if notification and not isinstance(notification, dict):
        faults.append('notification must be a dict')
        return
    for key in notification.keys():
        if key not in NOTIFICATIONS_META.keys():
            faults.append('%s is invalid field. valid fields are %s' % (key, str(NOTIFICATIONS_META.keys())))
    for key in NOTIFICATIONS_META.keys():
        if key not in notification.keys():
            faults.append('%s is missing from input.' % key)
    for key in notification.keys():
        if not validate_boolean(notification[key]):
            faults.append('\'%s\' field with value \'%s\' must has a boolean value' % (key, notification[key]))


def validate_date_in_the_future(due_date, faults):
    if not due_date or not isinstance(due_date, int):
        faults.append('due_date must be none empty int')
        return
    now = int(time.time())
    if due_date < now + MIN_DUE_DATE_SECONDS or due_date > now + MAX_DUE_DATE_SECONDS:
        faults.append('Invalid due date. Due date must be in the range %d - %d seconds. Current value is %d' % (
            now + MIN_DUE_DATE_SECONDS, now + MAX_DUE_DATE_SECONDS, due_date))


def validate_task_description(task_description, faults):
    if not validate_len_in_range(task_description, TASK_DESCRIPTION_MIN, TASK_DESCRIPTION_MAX):
        faults.append('%s is not a valid description. description length should be in the range %d - %d' % (
            task_description, TASK_DESCRIPTION_MIN, TASK_DESCRIPTION_MAX))


def validate_task_title(task_title, faults):
    if not validate_len_in_range(task_title, TASK_TITLE_MIN, TASK_TITLE_MAX):
        faults.append('%s is not a valid title. title length should be in the range %d - %d' % (
            task_title, TASK_TITLE_MIN, TASK_TITLE_MAX))


def validate_facebook_id(facebook_id, faults):
    if not facebook_id or not (isinstance(facebook_id, str) or isinstance(facebook_id, unicode)):
        faults.append('facebook_id must be a none empty string')
        return
    if len(facebook_id) <= FB_ID_MIN_LENGTH or len(facebook_id) > FB_ID_MAX_LENGTH:
        faults.append('facebook_id must be between {}-{} characters'.format(FB_ID_MIN_LENGTH, FB_ID_MAX_LENGTH))
    if not facebook_id.isdigit():
        faults.append('facebook_id must be all digits')


def validate_facebook_access_token(fb_access_token, faults):
    if not fb_access_token or not (isinstance(fb_access_token, str) or isinstance(fb_access_token, unicode)):
        faults.append('fb_access_token must be a none empty string')
        return
    if len(fb_access_token) < FB_TOKEN_MIN_LENGTH:
        faults.append('fb_access_token must be atleast {} characters'.format(FB_TOKEN_MIN_LENGTH))


USER_META = {
    'first_name': (validate_first_name, MANDATORY),
    'last_name': (validate_last_name, MANDATORY),
    'user_name': validate_user_name,
    'password': validate_password,
    'email': (validate_email, MANDATORY),
    'phone_number': validate_phone_number,
    'role': (validate_user_role, MANDATORY),
    'facebook_id': validate_facebook_id,
    'facebook_access_token': validate_facebook_access_token,
    'notifications': validate_notifications,
}

CASE_META = {
    'title': (validate_title, MANDATORY),
    'description': (validate_description, MANDATORY),
    'petitioner_id': (noop, MANDATORY),
    'tasks': (validate_tasks, MANDATORY),
    'state': (validate_case_state, not MANDATORY),
    'location': (location_validator.validate_location, not MANDATORY)
}

TASK_META = {
    'location': None,
    'destination': None,
    'volunteer_id': None,
    'description': (validate_task_description, MANDATORY),
    'title': (validate_task_title, MANDATORY),
    'state': validate_task_state,
    'type': (validate_task_type, MANDATORY),
    'due_date': (validate_date_in_the_future, MANDATORY),
    'created_at': None,
    'updated_at': None,
    'duration': None,
    'id': validate_task_id
}

NOTIFICATIONS_META = {
    'sms': None,
    'email': None
}


def entity_exists(collection_name, entity_id):
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
    if 'state' in updated_case:
        _validate_status_transition(current_case['state'], updated_case['state'], VALID_CASE_STATES, CASE_TRANSITIONS,
                                    faults)
        if faults:
            return
        if updated_case.get('tasks'):
            validate_tasks(updated_case['tasks'], faults, current_tasks=current_case['tasks'])
        if updated_case['state'] == CASE_COMPLETED and len(updated_case['tasks']) != sum(
                1 for task in updated_case['tasks'] if task['state'] == TASK_COMPLETED):
            faults.append(
                'A case cant be marked as %s until all tasks are marked as %s' % (CASE_COMPLETED, TASK_COMPLETED))

    elif 'tasks' in updated_case:
        validate_tasks(updated_case['tasks'], faults, current_case['tasks'])


def case_post_validate(payload, faults):
    validate_mandatory_and_present_fields(payload, CASE_META, faults)
    if faults:
        return
    validate_petitioner_id(payload['petitioner_id'], faults)


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
            faults.append(
                'The field \'%s\' in invalid field. Valid field names are: %s' % (field_name, str(meta.keys())))
    if faults:
        return
    for field_name, field_validator in meta.iteritems():
        if field_name in payload and field_validator:
            field_validator(payload[field_name], faults)
