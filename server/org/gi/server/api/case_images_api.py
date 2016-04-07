from googleapiclient import discovery
from googleapiclient import http
from oauth2client.client import GoogleCredentials
from flask import request
from io import BytesIO
from flask_restful import Resource
from org.gi.server import utils as u
from org.gi.server.db import db

_BUCKET = 'mineral-weaver-122811'
_ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


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
        resp = self._upload_object(request.files['file'].read(), final_file_name)
        return {'id': resp['id'],
                'image_url': 'https://storage.googleapis.com/%s/%s' % (_BUCKET, final_file_name)}, u.HTTP_CREATED

    def _put(self, case_id, image_id):
        print('put ' + case_id + '  ' + image_id)

    def _get(self, case_id, image_id):
        print('get ' + case_id + '  ' + image_id)

    def delete(self, case_id, image_id):
        print('delete ' + case_id + '  ' + image_id)
        if not u.is_valid_db_id(case_id):
            return ['%s is not a valid case id ' % case_id], u.HTTP_BAD_INPUT
        if not self._validate_case(case_id):
            return ['Can not find a case with id %s' % case_id], u.HTTP_NOT_FOUND
        self._delete_object(image_id)
        return {}, u.HTTP_NO_CONTENT


    def _validate_case(self, case_id):
        return db.cases.find_one({'_id': u.to_object_id(case_id)})

    def _create_service(self):
        credentials = GoogleCredentials.get_application_default()
        return discovery.build('storage', 'v1', credentials=credentials)

    def _upload_object(self, data, filename):
        service = self._create_service()

        # This is the request body as specified:
        # http://g.co/cloud/storage/docs/json_api/v1/objects/insert#request
        body = {
            'name': filename,
            'acl': [{
                'entity': 'allUsers',
                'role': 'READER'
                }
            ]
        }
        # Now insert them into the specified bucket as a media insertion.
        # http://g.co/dev/resources/api-libraries/documentation/storage/v1/python/latest/storage_v1.objects.html#insert
        bio = BytesIO(data)
        media = http.MediaIoBaseUpload(
            bio,
            'application/octet-stream'
        )
        req = service.objects().insert(bucket=_BUCKET, body=body, media_body=media)
        return req.execute()

    def _get_object(self, filename, out_file):
        service = self._create_service()
        # Use get_media instead of get to get the actual contents of the object.
        # http://g.co/dev/resources/api-libraries/documentation/storage/v1/python/latest/storage_v1.objects.html#get_media
        req = service.objects().get_media(bucket=_BUCKET, object=filename)

        downloader = http.MediaIoBaseDownload(out_file, req)

        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download {}%.".format(int(status.progress() * 100)))

        return out_file

    def _delete_object(self, filename):
        service = self._create_service()
        req = service.objects().delete(bucket=_BUCKET, object=filename)
        return req.execute()

