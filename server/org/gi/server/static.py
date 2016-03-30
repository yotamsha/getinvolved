from flask import send_from_directory, Blueprint,make_response
from sys import platform as _platform
import org.gi.server.validation.field_constraints as fc
import os
import json
import org.gi.server.utils as u


static_bp = Blueprint('static_bp', __name__)


def _get_static_folder(_type):
    if _platform in ['darwin', 'linux2', 'linux']:
        path_array = os.getcwd().split('/')
        path_array = path_array[:len(path_array) - 3]
        path_array.append('static')
        path_array.append(_type)
        return '/'.join(path_array)
    else:
        file_path = '..\..\..%sstatic%s%s' % (os.path.sep, os.path.sep, _type)
        return file_path


@static_bp.route('/html/<path:path>')
def send_html(path):
    return send_from_directory(_get_static_folder('html'), path)


@static_bp.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(_get_static_folder('css'), path)


@static_bp.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(_get_static_folder('js'), path)

@static_bp.route('/api/misc/constraints')
def get_fields_len_constraints():
    resp = make_response(json.dumps(fc.LENGTH_CONSTRAINTS), u.HTTP_OK)
    resp.headers.extend({'Content-Type': 'application/json'})
    return resp
