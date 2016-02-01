from flask import request, abort
from flask_restful import Resource, reqparse

from org.gi.server.db import db
from org.gi.server import utils as u


class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(UserList, self).__init__()

    #@requires_roles(auth.ROLE_ADMIN)
    def get(self):
        try:
            _filter, projection, sort, page_size_str, page_number_str = u.get_fields_projection_and_filter(request)
            users = db.users.find(projection=projection, filter=_filter)
            users = u.handle_sort_and_paging(users, sort, page_size_str, page_number_str)
        except Exception as e:
            abort(u.HTTP_SERVER_ERROR, str(e))
        return u.make_list(users), u.HTTP_OK
