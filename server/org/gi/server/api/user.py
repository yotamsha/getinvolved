from flask import request, abort
from flask_restful import Resource, reqparse

import org.gi.server.authorization as auth
from org.gi.server import validations as v
from org.gi.server.authorization import requires_auth
from org.gi.server import utils as u
from org.gi.server.db import db
from org.gi.server.log import log


class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(UserList, self).__init__()

    # @requires_roles(auth.ROLE_ADMIN)
    @requires_auth
    def get(self):
        try:
            _filter, projection, sort, page_size_str, page_number_str = u.get_fields_projection_and_filter(request)
            users = db.users.find(projection=projection, filter=_filter)
            users = u.handle_sort_and_paging(users, sort, page_size_str, page_number_str)
        except Exception as e:
            abort(u.HTTP_SERVER_ERROR, str(e))
        return u.make_list(users), u.HTTP_OK


class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(User, self).__init__()

    def _pad_with_roles(self, payload):
        if payload and isinstance(payload, dict) and not payload.get('role'):
            payload['role'] = auth.USER

    @requires_auth
    def get(self, user_id):
        try:
            user = db.users.find_one({'_id': u.to_object_id(user_id)})
            u.handle_id(user)
        except Exception as e:
            abort(u.HTTP_NOT_FOUND, str(e))
        return user, u.HTTP_OK

    @requires_auth
    def delete(self, user_id):
        try:
            result = db.users.delete_one({'_id': u.to_object_id(user_id)})
            if result.deleted_count != 1:
                raise Exception('One user should be deleted but %d users were deleted' % result.deleted_count)
        except Exception as e:
            return str(e), u.HTTP_NOT_FOUND
        return '', u.HTTP_NO_CONTENT

    @requires_auth
    def post(self):
        faults = []
        payload = request.json
        self._pad_with_roles(payload)
        v.post_validate(payload, v.USER_META, faults)
        if faults:
            log.debug("Failed to create a user. Faults: %s", str(faults))
            return {'errors': faults}, u.HTTP_BAD_INPUT
        try:
            user = request.json
            user['password'] = auth.hash_password(user['password'])
            id = db.users.insert(user)
        except Exception as e:
            abort(u.HTTP_BAD_INPUT, str(e))
        created = db.users.find_one({'_id': u.to_object_id(id)})
        u.handle_id(created)
        return created, u.HTTP_CREATED

    @requires_auth
    def put(self, user_id):
        user = db.users.find_one({'_id': u.to_object_id(user_id)})
        if not user:
            return 'Could not find a user with id %s' % user_id, u.HTTP_NOT_FOUND
        else:
            faults = []
            payload = request.json
            self._pad_with_roles(payload)
            v.put_validate(payload, v.USER_META, faults)
            if faults:
                return {'errors': faults}, u.HTTP_BAD_INPUT
            try:
                result = db.users.update_one({'_id': u.to_object_id(user_id)}, request.json)
                if result.modified_count != 1:
                    msg = '%d users where modified. One user only should be modified.' % result.modified_count
                    raise Exception(msg)
            except Exception as e:
                abort(u.HTTP_BAD_INPUT, str(e))
            return '', u.HTTP_NO_CONTENT