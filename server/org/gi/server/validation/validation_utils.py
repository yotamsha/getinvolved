# Extracting general use functions to separate module to overcome circular imports


def validate_len_in_range(value, _min, _max):
    return value and _min <= len(value.strip()) <= _max


def validate_number_in_range(number, _min, _max):
    return number and is_a_number(number) and (_min <= number <= _max)


def is_a_number(number):
    return isinstance(number, (int, long, float))


def is_a_list(_list):
    return _list and isinstance(_list, list)


def validate_mandatory_and_present_fields(payload, meta, faults, mandatory=True):
    FUNC_INDEX = 0
    MANDATORY_INDEX = 1
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