#!/usr/bin/env bash

#
# package GI web client and copy it the Apache under GCE instance, unpack it on the GCE instance
#

set -x

ZONE=europe-west1-b
CLIENT_ARCHIVE=get_involved_client.tar.gz
INSTANCE_NAME=gi-server
REMOTE_SCRIPT=client_remote_deploy.sh
REMOTE_PATH=/var/wwww/html

python zipit.py ${CLIENT_ARCHIVE} ./app
echo $?
gcloud compute copy-files ./${CLIENT_ARCHIVE} ${INSTANCE_NAME}:~/ --zone ${ZONE}
echo $?
gcloud compute copy-files ./${REMOTE_SCRIPT} ${INSTANCE_NAME}:~/ --zone ${ZONE}
echo $?
rm -rf ${CLIENT_ARCHIVE}
echo $?
# run remote script
gcloud compute ssh ${INSTANCE_NAME} --zone ${ZONE} chmod +x ./${REMOTE_SCRIPT}
echo $?
gcloud compute ssh ${INSTANCE_NAME} --zone ${ZONE}  ./${REMOTE_SCRIPT}
echo $?






