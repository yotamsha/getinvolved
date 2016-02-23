__author__ = 'avishayb'

from bson.objectid import ObjectId
import urllib
import pymongo
from functools import wraps
from flask import request
import logging

SORT_ORDER = {
    'ASCENDING': pymongo.ASCENDING,
    'DESCENDING': pymongo.DESCENDING,
    'ASC': pymongo.ASCENDING,
    'DESC': pymongo.DESCENDING,
    'ascending': pymongo.ASCENDING,
    'descending': pymongo.DESCENDING,
    'asc': pymongo.ASCENDING,
    'desc': pymongo.DESCENDING
}

MIME_JSON = 'application/json'

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
HTTP_BAD_INPUT = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_METHOD_NOT_ALLOWED = 405
HTTP_CONFLICT = 409
HTTP_SERVER_ERROR = 500
HTTP_SERVICE_UNAVAILABLE = 503
HTTP_GATEWAY_TIMEOUT = 504




def web_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.error('%s : %s : %s' % (str(request), str(request.remote_addr), str(request.user_agent)))
        return func(*args, **kwargs)
    return wrapper

def handle_sort_and_paging(cursor, sort, page_size_str, page_number_str):
    if cursor:
        sort = sort if sort else [('_id', pymongo.ASCENDING)]
        cursor = cursor.sort(sort)
        page_size = as_int(page_size_str)
        if page_size and isinstance(page_size, int) and page_size > 0:
            cursor = cursor.limit(page_size)
            page_number = as_int(page_number_str)
            if page_number and isinstance(page_number, int) and page_number >= 0:
                cursor = cursor.skip(page_number * page_size)
    return cursor


def handle_id(record):
    if record and '_id' in record:
        record['id'] = str(record['_id'])
        del record['_id']


def to_object_id(record_id):
    return ObjectId(record_id)


def diff_dict(original, modified):
    if isinstance(original, dict) and isinstance(modified, dict):
        changes = {}
        for key, value in modified.iteritems():
            if isinstance(value, dict):
                inner_dict = diff_dict(original[key], modified[key])
                if inner_dict != {}:
                    changes[key] = {}
                    changes[key].update(inner_dict)
            else:
                if original.has_key(key):
                    if value != original[key]:
                        changes[key] = value
                else:
                    changes[key] = value

        return changes
    else:
        raise Exception('parameters must be a dictionary')


def as_int(str):
    try:
        return int(str)
    except Exception:
        return None


def make_list(cursor):
    lst = []
    for entity in cursor:
        handle_id(entity)
        lst.append(entity)
    return lst


def query_string_to_dict(request):
    if not request:
        return None
    if not request.query_string:
        return None
    _args = request.query_string.split('&')
    _result = dict()
    if _args:
        for arg in _args:
            index = arg.find('=')
            if index != -1:
                _result[arg[:index]] = arg[index + 1:]
    return _result


def get_fields_projection_and_filter(request):
    def _get_sort_args():
        if not _result or not _result.get('sort'):
            return None
        sort = eval(urllib.unquote(_result.get('sort')).decode('utf8'))
        result = []
        if not sort or not isinstance(sort, list):
            return None
        for sort_item in sort:
            if not isinstance(sort_item, tuple):
                return None
            if len(sort_item) != 2 or sort_item[1] not in SORT_ORDER.keys():
                return None
            result.append((sort_item[0], SORT_ORDER[sort_item[1]]))
        return result

    if not request:
        return None, None, None, None, None
    if not request.query_string:
        return None, None, None, None, None
    _args = request.query_string.split('&')
    _result = dict()
    if _args:
        for arg in _args:
            index = arg.find('=')
            if index != -1:
                _result[arg[:index]] = arg[index + 1:]
    _filter = eval(urllib.unquote(_result.get('filter')).decode('utf8')) if _result.get('filter') else None
    _projection = {field_name: 1 for field_name in _result.get('projection').split(',')} if _result.get(
        'projection') else None
    _sort = _get_sort_args()
    return _filter, _projection, _sort, _result.get("page_size"), _result.get("page_number")


class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]
