from flask import request
from flask_restful import Resource
from org.gi.server import utils as u
from org.gi.server.db import db
from org.gi.server.service.google.google_service import GoogleService

_ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
_BUCKET = 'mineral-weaver-122811'


class CaseImagesApi(Resource):
    def post(self, case_id):
        print('post ' + case_id)
        if not u.is_valid_db_id(case_id):
            return ['%s is not a valid case id ' % case_id], u.HTTP_BAD_INPUT
        if not self._validate_case(case_id):
            return ['Can not find a case with id %s' % case_id], u.HTTP_NOT_FOUND
        request_data = u.query_string_to_dict(request)
        if not request or not request_data.get('file_name'):
            return ['File name must be specified as a query argument'], u.HTTP_BAD_INPUT
        file_name = request_data.get('file_name')
        dot_index = file_name.rfind('.')
        if dot_index == -1:
            return ['File name must contain extension'], u.HTTP_BAD_INPUT
        ext = file_name[dot_index + 1:]
        if not ext:
            return ['File name must contain extension'], u.HTTP_BAD_INPUT
        if not ext.lower() in _ALLOWED_EXTENSIONS:
            return ['Invalid file extension %s, Supported extension are %s' % (
                ext, str(_ALLOWED_EXTENSIONS))], u.HTTP_BAD_INPUT
        final_file_name = case_id + '_' + file_name
        resp = GoogleService().upload_object(request.files['file'].read(), final_file_name, _BUCKET)
        return {'id': resp['id'],
                'image_url': 'https://storage.googleapis.com/%s/%s' % (_BUCKET, final_file_name)}, u.HTTP_CREATED

    def delete(self, case_id, image_id):
        print('delete ' + case_id + '  ' + image_id)
        if not u.is_valid_db_id(case_id):
            return ['%s is not a valid case id ' % case_id], u.HTTP_BAD_INPUT
        if not self._validate_case(case_id):
            return ['Can not find a case with id %s' % case_id], u.HTTP_NOT_FOUND
        GoogleService().delete_object(image_id, _BUCKET)
        return {}, u.HTTP_NO_CONTENT

    def _validate_case(self, case_id):
        return db.cases.find_one({'_id': u.to_object_id(case_id)})

    def _put(self, case_id, image_id):
        print('put ' + case_id + '  ' + image_id)

    def _get(self, case_id, image_id):
        print('get ' + case_id + '  ' + image_id)