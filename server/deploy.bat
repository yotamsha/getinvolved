::
:: Deploy GI server to GCE
::

@ECHO ON
SET ZONE=europe-west1-b
SET SERVER_ARCHIVE=get_involved_server-1.0.tar.gz
SET INSTANCE_NAME=gi-server
SET REMOTE_SCRIPT=remote_deploy.sh

:: clean dist folder
RMDIR /S /Q dist

:: create the archive
python setup.py sdist --formats=gztar

call gcloud compute copy-files dist/%SERVER_ARCHIVE% %INSTANCE_NAME%: --zone %ZONE%

:: copy remote script to GCE
call gcloud compute copy-files %REMOTE_SCRIPT% %INSTANCE_NAME%: --zone %ZONE%

::  run remote script
call gcloud compute ssh %INSTANCE_NAME% --zone %ZONE%  chmod +x ./%REMOTE_SCRIPT%
call gcloud compute ssh %INSTANCE_NAME% --zone %ZONE%   ./%REMOTE_SCRIPT%


