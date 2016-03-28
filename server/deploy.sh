#!/usr/bin/env bash

#
# Deploy GI server to GCE
#
set -x


ZONE=europe-west1-b
SERVER_ARCHIVE=get_involved_server-1.0.tar.gz
INSTANCE_NAME=gi-server
REMOTE_SCRIPT=remote_deploy.sh

# clean dist folder
sudo rm -rf ./dist
echo $?
# create the archive
sudo python setup.py sdist
echo $?

# copy archive to GCE
gcloud compute copy-files ./dist/${SERVER_ARCHIVE} ${INSTANCE_NAME}:~/ --zone ${ZONE}
echo $?

#copy remote script to GCE
gcloud compute copy-files ${REMOTE_SCRIPT} ${INSTANCE_NAME}:~/ --zone ${ZONE}
echo $?

# run remote script
gcloud compute ssh ${INSTANCE_NAME} --zone ${ZONE}  chmod +x ./${REMOTE_SCRIPT}
echo $?
gcloud compute ssh ${INSTANCE_NAME} --zone ${ZONE}   ./${REMOTE_SCRIPT}
echo $?
