import uuid

from flask import request, abort
from flask_restful import Resource, reqparse

from org.gi.server import location as l
from org.gi.server import utils as u
from org.gi.server.authorization import requires_auth
from org.gi.server.db import db
from org.gi.server.log import log
from org.gi.server.validation import validations as v
from org.gi.server.validation.case_state_machine import CASE_PENDING_APPROVAL, CASE_UNDEFINED, CASE_ASSIGNED, \
    CASE_PENDING_INVOLVEMENT, CASE_COMPLETED, CASE_PARTIALLY_ASSIGNED, CASE_PARTIALLY_COMPLETED
from org.gi.server.validation.task_state_machine import TASK_PENDING, TASK_ASSIGNED, TASK_COMPLETED


class Case(Resource):
    @staticmethod
    def _handle_geo_location(case):
        if 'tasks' not in case:
            return
        fields = ['destination_address', 'address']
        for task in case['tasks']:
            for field in fields:
                address = task.get(field)
                if address:
                    geo = l.get_lat_lng(address)
                    address['geo'] = geo

    def get(self, case_id):
        try:
            case = db.cases.find_one({'_id': u.to_object_id(case_id)})
            u.handle_id(case)
        except Exception as e:
            abort(u.HTTP_NOT_FOUND, str(e))
        return case, u.HTTP_OK

    @requires_auth
    def delete(self, case_id):
        try:
            result = db.cases.delete_one({'_id': u.to_object_id(case_id)})
            if result.deleted_count != 1:
                raise Exception('One case should be deleted but %d cases were deleted' % result.deleted_count)
        except Exception as e:
            return str(e), u.HTTP_NOT_FOUND
        return '', u.HTTP_NO_CONTENT

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
                incoming_case = self.__prep_case_before_update(request.json, case)
                result = db.cases.update_one({"_id": u.to_object_id(case_id)}, {'$set': incoming_case})
                if result.modified_count != 1:
                    msg = '%d cases where modified. One case only should be modified. \
                     Case details: id: %s data for update %s' % (result.modified_count, case_id, str(incoming_case))
                    raise Exception(msg)
            except Exception as e:
                log.debug("Failed to update a case. Exception:: %s", str(e))
                abort(u.HTTP_BAD_INPUT, str(e))
            return '', u.HTTP_NO_CONTENT

    def __prep_case_before_update(self, updated_case, db_case):
        if updated_case.get('tasks'):
            updated_case['state'] = self.__get_updated_case_state(updated_case.get('tasks'), db_case.get('state'))
        self._handle_geo_location(updated_case)
        return updated_case

    def __get_updated_case_state(self, tasks, curr_case_state):
        ALL_TASKS_SAME_STATE = {
            TASK_PENDING: CASE_PENDING_INVOLVEMENT,
            TASK_ASSIGNED: CASE_ASSIGNED,
            TASK_COMPLETED: CASE_COMPLETED
        }

        task_states = set()
        updated_case_state = ''
        for task in tasks:
            task_states.add(task['state'])
        if len(task_states) == 1:
            updated_case_state = ALL_TASKS_SAME_STATE.get(task_states.pop())
        elif len(task_states) == 2:
            if {TASK_PENDING, TASK_ASSIGNED}.issubset(task_states):
                updated_case_state = CASE_PARTIALLY_ASSIGNED
            if {TASK_COMPLETED, TASK_ASSIGNED}.issubset(task_states):
                updated_case_state = CASE_PARTIALLY_COMPLETED

        return updated_case_state if updated_case_state else curr_case_state

    @requires_auth
    def post(self):
        faults = []
        v.case_post_validate(request.json, faults)
        if faults:
            log.debug("Failed to create a case. Faults: %s", str(faults))
            return {'errors': faults}, u.HTTP_BAD_INPUT
        try:
            case = self.__prep_case_before_insert(request.json)
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

    def __prep_case_before_insert(self, case):
        if not 'state' in case or case['state'] == CASE_UNDEFINED:
            case['state'] = CASE_PENDING_APPROVAL
        for task in case['tasks']:
            task['id'] = str(uuid.uuid4())
            task['state'] = TASK_PENDING
        self._handle_geo_location(case)
        return case


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