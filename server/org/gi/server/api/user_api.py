from flask import request, abort, session
from flask_restful import Resource, reqparse

import org.gi.server.authorization as auth
from org.gi.server import utils as u
from org.gi.server.authorization import requires_auth
from org.gi.server.db import db
from org.gi.server.log import log
from org.gi.server.validation import validations as v


class UserListApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(UserListApi, self).__init__()

    @u.web_log
    @requires_auth
    def get(self):
        try:
            _filter, projection, sort, page_size_str, page_number_str = u.get_fields_projection_and_filter(request)
            users = db.users.find(projection=projection, filter=_filter)
            users = u.handle_sort_and_paging(users, sort, page_size_str, page_number_str)
        except Exception as e:
            abort(u.HTTP_SERVER_ERROR, str(e))
        return u.make_list(users), u.HTTP_OK


class UserApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(UserApi, self).__init__()

    def _pad_with_roles(self, payload):
        if payload and isinstance(payload, dict) and not payload.get('role'):
            payload['role'] = auth.NONE

    @u.web_log
    @requires_auth
    def get(self, user_id):
        try:
            if 'me' == user_id:
                user_id = session['user']['_id']
            user = db.users.find_one({'_id': u.to_object_id(user_id)})
            u.handle_id(user)
        except Exception as e:
            abort(u.HTTP_NOT_FOUND, str(e))
        return user, u.HTTP_OK

    @u.web_log
    @requires_auth
    def delete(self, user_id):
        try:
            result = db.users.delete_one({'_id': u.to_object_id(user_id)})
            if result.deleted_count != 1:
                raise Exception('One user should be deleted but %d users were deleted' % result.deleted_count)
        except Exception as e:
            return str(e), u.HTTP_NOT_FOUND
        return '', u.HTTP_NO_CONTENT

    @u.web_log
    def post(self):
        faults = []
        payload = request.json
        self._pad_with_roles(payload)
        v.user_post_validate(payload, faults)
        if faults:
            log.debug("Failed to create a user. Faults: %s", str(faults))
            return {'errors': faults}, u.HTTP_BAD_INPUT
        try:
            user = request.json
            if 'password' in user:
                user['password'] = auth.hash_password(user['password'])
            id = db.users.insert(user)
        except Exception as e:
            abort(u.HTTP_BAD_INPUT, str(e))
        created = db.users.find_one({'_id': u.to_object_id(id)})
        u.handle_id(created)
        return created, u.HTTP_CREATED

    @u.web_log
    @requires_auth
    def put(self, user_id):
        user = db.users.find_one({'_id': u.to_object_id(user_id)})
        if not user:
            return 'Could not find a user with id %s' % user_id, u.HTTP_NOT_FOUND
        else:
            faults = []
            payload = request.json
            self._pad_with_roles(payload)
            v.user_put_validate(payload, faults)
            if faults:
                return {'errors': faults}, u.HTTP_BAD_INPUT
            try:
                db.users.update_one({'_id': u.to_object_id(user_id)}, request.json)
            except Exception as e:
                abort(u.HTTP_BAD_INPUT, str(e))
            return self.get(user_id)