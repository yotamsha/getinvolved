from flask import request, abort
from flask_restful import Resource, reqparse

from org.gi.server import utils as u
from org.gi.server.authorization import requires_auth
from org.gi.server.db import db
from org.gi.server.log import log
from org.gi.server.model.Case import Case

import org.gi.server.validation.validations as v


class CaseApi(Resource):
    @u.web_log
    def get(self, case_id):
        try:
            request_data = u.query_string_to_dict(request)
            case = db.cases.find_one({'_id': u.to_object_id(case_id)})
            Case.prep_case_for_client(case, add_volunteer_attributes=(request_data and request_data.get(
                'add_volunteer_attributes') is not None))
        except Exception as e:
            abort(u.HTTP_NOT_FOUND, str(e))
        return case, u.HTTP_OK

    @u.web_log
    @requires_auth
    def put(self, case_id):
        case = db.cases.find_one({'_id': u.to_object_id(case_id)})
        if not case:
            return 'Could not find a user with id %s' % case_id, u.HTTP_NOT_FOUND
        else:
            faults = []
            v.case_put_validate(case, request.json, faults)
            if faults:
                log.debug("Failed to update a case. Faults: %s", str(faults))
                return {'errors': faults}, u.HTTP_BAD_INPUT
            try:
                incoming_case = Case.prep_case_before_update(request.json, case)
                db.cases.update_one({"_id": u.to_object_id(case_id)}, {'$set': incoming_case})
            except Exception as e:
                log.debug("Failed to update a case. Exception:: %s", str(e))
                abort(u.HTTP_BAD_INPUT, str(e))
            return self.get(case_id)

    @u.web_log
    @requires_auth
    def post(self):
        faults = []
        v.case_post_validate(request.json, faults)
        if faults:
            log.debug("Failed to create a case. Faults: %s", str(faults))
            return {'errors': faults}, u.HTTP_BAD_INPUT
        try:
            case = Case.prep_case_before_insert(request.json)
            _id = db.cases.insert(case)
        except Exception as e:
            abort(u.HTTP_BAD_INPUT, str(e))
        created = db.cases.find_one({'_id': u.to_object_id(_id)})
        if not created:
            msg = 'Failed to find a newly created case. Using id %s' % u.to_object_id(_id)
            log.debug(msg)
            abort(u.HTTP_SERVER_ERROR, msg)
        Case.prep_case_for_client(created)
        return created, u.HTTP_CREATED


class CaseListApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(CaseListApi, self).__init__()

    @u.web_log
    def get(self):
        try:
            _filter, projection, sort, page_size_str, page_number_str, _count = u.get_fields_projection_and_filter(request)
            cases = db.cases.find(projection=projection, filter=_filter)
            count = None
            if _count:
                count = cases.count()
            else:
                cases = u.handle_sort_and_paging(cases, sort, page_size_str, page_number_str)
                if cases and sort:
                    cases = cases.sort(sort)
        except ValueError as e:
            abort(u.HTTP_BAD_INPUT, str(e))
        except Exception as e:
            abort(u.HTTP_SERVER_ERROR, str(e))
        if not count:
            cases = u.make_list(cases)
            for case in cases:
                Case.prep_case_for_client(case)
            return cases, u.HTTP_OK
        else:
            return {'count': count}, u.HTTP_OK
