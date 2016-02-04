import os
import json
from sys import platform as _platform

from flask import Flask, send_from_directory, make_response, request, jsonify
from flask_restful import Api
from authomatic.adapters import WerkzeugAdapter as adapter
from authomatic import Authomatic
from org.gi.server.auth.config import config as auth_config

authomatic = Authomatic(auth_config, "THE MOSTESTSECRETSTRINGY", report_errors=True)

from org.gi.server import utils as u

from org.gi.server.model.case import Case
from org.gi.server.model.caselist import CaseList
from org.gi.server.model.user import User
from org.gi.server.model.userlist import UserList

app = Flask(__name__, static_url_path='')
api = Api(app)


@app.route('/login/<provider_name>', methods=['GET', 'POST'])
def login(provider_name):
    response = make_response()
    result = authomatic.login(adapter(request, response), provider_name)
    if result and result.user:
        result.user.update()
        return jsonify(json.loads(result.user.content))
    return response


def _get_static_folder(_type):
    if _platform in ['darwin', 'linux2', 'linux']:
        path_array = os.getcwd().split('/')
        path_array = path_array[:len(path_array) - 3]
        path_array.append('static')
        path_array.append(_type)
        return '/'.join(path_array)
    else:
        return '..\..\..%sstatic%s%s' % (os.path.sep, os.path.sep, _type)


@app.route('/html/<path:path>')
def send_html(path):
    return send_from_directory(_get_static_folder('html'), path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(_get_static_folder('css'), path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(_get_static_folder('js'), path)


@app.route('/api/ping')
def ping():
    return 'Pong', u.HTTP_OK


api.add_resource(UserList, '/api/users')
api.add_resource(CaseList, '/api/cases')

api.add_resource(User, '/api/users/<string:user_id>', '/api/users')
api.add_resource(Case, '/api/cases/<string:case_id>', '/api/cases')

if __name__ == '__main__':
    app.run(debug=True)
