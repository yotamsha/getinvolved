
#
# package GI web client and copy it the Apache under GCE instance, unpack it on the GCE instance
#

@ECHO ON
SET ZONE=europe-west1-b
SET CLIENT_ARCHIVE=get_involved_client.tar.gz
SET INSTANCE_NAME=gi-server
SET REMOTE_SCRIPT=client_remote_deploy.sh
SET REMOTE_PATH=/var/wwww/html

DEL %CLIENT_ARCHIVE%
ECHO zipping file.
python zipit.py %CLIENT_ARCHIVE% ./app
ECHO copying archive to instance.
call gcloud compute copy-files ./%CLIENT_ARCHIVE% root@%INSTANCE_NAME%:/ --zone %ZONE%
ECHO copying script to instance.
call gcloud compute copy-files ./%REMOTE_SCRIPT% root@%INSTANCE_NAME%:/ --zone %ZONE%
ECHO deleting archive.
DEL %CLIENT_ARCHIVE%

ECHO give access rights to remote script
call gcloud compute ssh %INSTANCE_NAME% --zone %ZONE% chmod +x /%REMOTE_SCRIPT%
ECHO run remote script
call gcloud compute ssh %INSTANCE_NAME% --zone %ZONE%  /%REMOTE_SCRIPT%
ECHO done!







