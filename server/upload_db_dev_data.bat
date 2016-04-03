::
:: Copy db_dev_data.py and dev_data folder to /home/<user>
:: Then clear database and run script
::

@ECHO ON
SET ZONE=europe-west1-b
SET INSTANCE_NAME=gi-server

call gcloud compute copy-files db_dev_data.py %INSTANCE_NAME%:/home/%USERNAME% --zone %ZONE%
call gcloud compute copy-files dev_data %INSTANCE_NAME%:/home/%USERNAME% --zone %ZONE%

call gcloud compute ssh %INSTANCE_NAME% --zone %ZONE%   python /home/%USERNAME%/db_dev_data.py -c
call gcloud compute ssh %INSTANCE_NAME% --zone %ZONE%   python /home/%USERNAME%/db_dev_data.py