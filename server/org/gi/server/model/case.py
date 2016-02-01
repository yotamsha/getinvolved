import uuid

from flask import request, abort
from flask_restful import Resource

from org.gi.server import validations as v
from org.gi.server import utils as u
from org.gi.server.db import db
from org.gi.server.log import log


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
            v.case_put_validate(case, request.json, faults)
            if faults:
                log.debug("Failed to update a case. Faults: %s", str(faults))
                return {'errors': faults}, u.HTTP_BAD_INPUT
            try:
                diff = u.diff_dict(case,request.json)
                result = db.users.update_one({"_id": case_id}, {'$set': diff})
                if result.modified_count != 1:
                    msg = '%d cases where modified. One case only should be modified.' % result.modified_count
                    raise Exception(msg)
            except Exception as e:
                log.debug("Failed to update a case. Exception:: %s", str(e))
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
