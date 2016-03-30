from org.gi.server.validation.field_constraints import LENGTH_CONSTRAINTS as LC

MIN_LEN = 0
MAX_LEN = 1

FUNC_INDEX = 0
MANDATORY_INDEX = 1

LEN_ERR_MSG_TEMPLATE = '%s is not a valid %s. %s length should be in the range %d - %d'


def validate_len_in_range(entity_name, field_name, value):
    return value and isinstance(value, basestring) and LC[entity_name][field_name][MIN_LEN] <= len(value.strip()) <= \
                                                       LC[entity_name][field_name][MAX_LEN]


def get_min_len(entity_name, field_name):
    return LC[entity_name][field_name][MIN_LEN]


def get_max_len(entity_name, field_name):
    return LC[entity_name][field_name][MAX_LEN]


def validate_number_in_range(number, _min, _max):
    return number and is_a_number(number) and (_min <= number <= _max)


def is_a_number(number):
    return number and isinstance(number, (int, long, float))


def is_a_list(_list):
    return _list and isinstance(_list, list)


def validate_mandatory_and_present_fields(payload, meta, faults, mandatory=True):
    if not payload or not isinstance(payload, dict):
        faults.append('payload must be none empty dict')
        return
    for key in payload.keys():
        if key not in meta.keys():
            faults.append('The field \'%s\' is invalid. Valid fields are %s' % (
                key, str(meta.keys())))
    for field_name, validation_info in meta.iteritems():
        if mandatory:
            if field_name not in payload and (isinstance(validation_info, tuple) and validation_info[MANDATORY_INDEX]):
                faults.append('The field %s is a mandatory field.' % field_name)
                continue
        if field_name in payload and validation_info:
            if isinstance(validation_info, tuple):
                validation_info[FUNC_INDEX](payload[field_name], faults)
            else:
                validation_info(payload[field_name], faults)