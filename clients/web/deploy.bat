
#
# package GI web client and copy it the Apache under GCE instance, unpack it on the GCE instance
#

@ECHO ON
SET ZONE=europe-west1-b
SET CLIENT_ARCHIVE=get_involved_client.tar.gz
SET INSTANCE=gi-server
SET REMOTE_SCRIPT=client_remote_deploy.sh
SET REMOTE_PATH=/var/wwww/html

DEL %CLIENT_ARCHIVE%
ECHO packaging client..
call grunt release
ECHO zipping file.
python zipit.py %CLIENT_ARCHIVE% ./dist/
ECHO copying archive to instance.
call gcloud compute copy-files %CLIENT_ARCHIVE% %INSTANCE%:/home/%USERNAME% --zone %ZONE%

ECHO copying script to instance.
call gcloud compute copy-files %REMOTE_SCRIPT% %INSTANCE%:/home/%USERNAME% --zone %ZONE%

ECHO deleting archive.
DEL %CLIENT_ARCHIVE%

ECHO give access rights to remote script
call gcloud compute ssh %INSTANCE% --zone %ZONE% chmod +x /home/%USERNAME%/%REMOTE_SCRIPT%
REM ECHO convert to LF line separator.
REM call gcloud compute ssh %INSTANCE% --zone %ZONE% dos2unix  /home/%USERNAME%/%REMOTE_SCRIPT% -c iso /home/%USERNAME%/%REMOTE_SCRIPT%
ECHO run remote script
call gcloud compute ssh %INSTANCE% --zone %ZONE% /home/%USERNAME%/%REMOTE_SCRIPT%
ECHO done!







