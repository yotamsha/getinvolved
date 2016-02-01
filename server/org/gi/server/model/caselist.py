from flask import request, abort
from flask_restful import Resource, reqparse

from org.gi.server.db import db
from org.gi.server import utils as u


class CaseList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(CaseList, self).__init__()

    def get(self):
        try:
            _filter, projection, sort, page_size_str, page_number_str = u.get_fields_projection_and_filter(request)
            cases = db.cases.find(projection=projection, filter=_filter)
            cases = u.handle_sort_and_paging(cases, sort, page_size_str, page_number_str)
            if cases and sort:
                cases = cases.sort(sort)
        except Exception as e:
            abort(u.HTTP_SERVER_ERROR, str(e))
        return u.make_list(cases), u.HTTP_OK