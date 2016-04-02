
#
# package GI web client and copy it the Apache under GCE instance, unpack it on the GCE instance
#

@ECHO ON
SET ZONE=europe-west1-b
SET CLIENT_ARCHIVE=get_involved_client.tar.gz
SET INSTANCE=gi-server
SET REMOTE_SCRIPT=client_remote_deploy.sh
SET REMOTE_PATH=/var/wwww/html
SET REMOTE_SCRIPT_PATH=/var/local

DEL %CLIENT_ARCHIVE%
ECHO packaging client..
call grunt release
ECHO zipping file.
python zipit.py %CLIENT_ARCHIVE% ./dist/
ECHO copying archive to instance.
call gcloud compute copy-files %CLIENT_ARCHIVE% %INSTANCE%:/home/%USERNAME% --zone %ZONE%

ECHO deleting archive.
DEL %CLIENT_ARCHIVE%

ECHO run remote script
call gcloud compute ssh %INSTANCE% --zone %ZONE% %REMOTE_SCRIPT_PATH%/%REMOTE_SCRIPT%
ECHO done!







