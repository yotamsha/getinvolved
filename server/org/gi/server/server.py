from flask import Flask, request, abort, send_from_directory
from flask_restful import Api, Resource, reqparse
from org.gi.config import config

import pymongo
from pymongo import IndexModel
import os
from org.gi.server import validations as v
from org.gi.server import utils as u
from sys import platform as _platform
import logging
import uuid


app = Flask(__name__, static_url_path='')
api = Api(app)
FORMAT = '%(asctime)-15s  %(message)s'
logging.basicConfig(format=FORMAT)
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


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


class Case(Resource):
    def get(self, case_id):
        try:
            case = db.cases.find_one({'_id': u.to_object_id(case_id)})
            u.handle_id(case)
        except Exception as e:
            abort(u.HTTP_NOT_FOUND, str(e))
        return case, u.HTTP_OK

    def delete(self, case_id):
        try:
            result = db.cases.delete_one({'_id': u.to_object_id(case_id)})
        except Exception as e:
            return str(e), u.HTTP_NOT_FOUND
        return '', u.HTTP_NO_CONTENT


    def put(self, case_id):
        case = db.cases.find_one({'_id': u.to_object_id(case_id)})
        if not case:
            return 'Could not find a user with id %s' % case_id, u.HTTP_NOT_FOUND
        else:
            faults = []
            v.case_put_validate(request.json, v.CASE_META, faults)
            if faults:
                return {'errors': faults}, u.HTTP_BAD_INPUT
            try:
                db.users.update_one({'_id': u.to_object_id(case_id)}, request.json)
            except Exception as e:
                abort(u.HTTP_BAD_INPUT, str(e))
            return '', u.HTTP_NO_CONTENT


    def post(self):
        faults = []
        v.case_post_validate(request.json, db, faults)
        if faults:
            log.debug("Failed to create a case. Faults: %s", str(faults))
            return {'errors': faults}, u.HTTP_BAD_INPUT
        try:
            case = request.json
            for task in case['tasks']:
                task['id'] = str(uuid.uuid4())
            _id = db.cases.insert(case)
        except Exception as e:
            abort(u.HTTP_BAD_INPUT, str(e))
        created = db.cases.find_one({'_id': u.to_object_id(_id)})
        if not created:
            msg = 'Failed to find a newly created case. Using id %s' % u.to_object_id(_id)
            log.debug(msg)
            abort(u.HTTP_SERVER_ERROR, msg)
        u.handle_id(created)
        return created, u.HTTP_CREATED


class CaseList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(CaseList, self).__init__()

    def get(self):
        try:
            _filter, projection = u.get_fields_projection_and_filter(request)
            cases = db.cases.find(projection=projection, filter=_filter)
        except Exception as e:
            abort(u.HTTP_SERVER_ERROR, str(e))
        return u.make_list(cases, 'cases'), u.HTTP_OK


class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(UserList, self).__init__()

    def get(self):
        try:
            # See https://docs.mongodb.org/manual/reference/operator/query/
            # http://127.0.0.1:5000/api/users?filter={"$and":[{"email":{"$eq":"dan@gi.net"}},{"email":{"$eq":"jack@gi.net"}}]}&projection=user_name,phone_number
            _filter, projection = u.get_fields_projection_and_filter(request)
            users = db.users.find(projection=projection, filter=_filter)
        except Exception as e:
            abort(u.HTTP_SERVER_ERROR, str(e))
        return u.make_list(users, 'users'), u.HTTP_OK


class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(User, self).__init__()

    def get(self, user_id):
        try:
            user = db.users.find_one({'_id': u.to_object_id(user_id)})
            u.handle_id(user)
        except Exception as e:
            abort(u.HTTP_NOT_FOUND, str(e))
        return user, u.HTTP_OK

    def delete(self, user_id):
        try:
            result = db.users.delete_one({'_id': u.to_object_id(user_id)})
            print('%d users were deleted' % result.deleted_count())
        except Exception as e:
            return str(e), u.HTTP_NOT_FOUND
        return '', u.HTTP_NO_CONTENT

    def post(self):
        faults = []
        v.post_validate(request.json, v.USER_META, faults)
        if faults:
            log.debug("Failed to create a user. Faults: %s", str(faults))
            return {'errors': faults}, u.HTTP_BAD_INPUT
        try:
            id = db.users.insert(request.json)
        except Exception as e:
            abort(u.HTTP_BAD_INPUT, str(e))
        created = db.users.find_one({'_id': u.to_object_id(id)})
        u.handle_id(created)
        return created, u.HTTP_CREATED

    def put(self, user_id):
        user = db.users.find_one({'_id': u.to_object_id(user_id)})
        if not user:
            return 'Could not find a user with id %s' % user_id, u.HTTP_NOT_FOUND
        else:
            faults = []
            v.put_validate(request.json, v.USER_META, faults)
            if faults:
                return {'errors': faults}, u.HTTP_BAD_INPUT
            try:
                db.users.update_one({'_id': u.to_object_id(user_id)}, request.json)
            except Exception as e:
                abort(u.HTTP_BAD_INPUT, str(e))
            return '', u.HTTP_NO_CONTENT

api.add_resource(UserList, '/api/users')
api.add_resource(CaseList, '/api/cases')

api.add_resource(User, '/api/users/<string:user_id>', '/api/users')
api.add_resource(Case, '/api/cases/<string:case_id>', '/api/cases')


def handle_constraints():
    email_index = IndexModel('email', name='email_index', unique=True)
    username_index = IndexModel('user_name', name='user_name_index', unique=True)
    phone_number_index = IndexModel(
        [("phone_number.number", pymongo.ASCENDING), ("phone_number.country_code", pymongo.ASCENDING)],
        name='phone_number_index', unique=True)
    db.users.create_indexes([email_index, phone_number_index, username_index])


if __name__ == '__main__':
    mongo = pymongo.MongoClient(config.get_db_uri())
    db = mongo.get_default_database()
    handle_constraints()
    app.run(debug=True)