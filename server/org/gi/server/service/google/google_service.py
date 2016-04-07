from googleapiclient import discovery
from googleapiclient import http
from oauth2client.client import GoogleCredentials
from io import BytesIO


class GoogleService:
    def __init__(self):
        pass

    @staticmethod
    def _create_service():
        credentials = GoogleCredentials.get_application_default()
        return discovery.build('storage', 'v1', credentials=credentials)

    def upload_object(self, data, filename, bucket):
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
        req = service.objects().insert(bucket=bucket, body=body, media_body=media)
        return req.execute()

    def get_object(self, filename, out_file, bucket):
        service = self._create_service()
        # Use get_media instead of get to get the actual contents of the object.
        # http://g.co/dev/resources/api-libraries/documentation/storage/v1/python/latest/storage_v1.objects.html#get_media
        req = service.objects().get_media(bucket=bucket, object=filename)

        downloader = http.MediaIoBaseDownload(out_file, req)

        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download {}%.".format(int(status.progress() * 100)))

        return out_file

    def delete_object(self, filename, bucket):
        service = self._create_service()
        req = service.objects().delete(bucket=bucket, object=filename)
        return req.execute()

