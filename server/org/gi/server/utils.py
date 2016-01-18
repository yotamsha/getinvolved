__author__ = 'avishayb'

from bson.objectid import ObjectId
import urllib


HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
HTTP_BAD_INPUT = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_SERVER_ERROR = 500


def handle_id(record):
    if record and '_id' in record:
        record['id'] = str(record['_id'])
        del record['_id']


def to_object_id(record_id):
    try:
        return ObjectId(record_id)
    except Exception as e:
        raise e


def make_list(cursor, name):
    lst = []
    for entity in cursor:
        handle_id(entity)
        lst.append(entity)
    return {name: lst}


def get_fields_projection_and_filter(request):
    if not request:
        return None, None
    if not request.query_string:
        return None, None
    _args = request.query_string.split('&')
    _result = dict()
    if _args:
        for arg in _args:
            index = arg.find('=')
            if index != -1:
                _result[arg[:index]] = arg[index + 1:]
    return eval(urllib.unquote(_result.get('filter')).decode('utf8')), {field_name: 1 for field_name in
                                                                        _result.get('projection').split(
                                                                            ',')} if _result.get(
        'projection') else {}

