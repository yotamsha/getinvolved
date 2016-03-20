#!/usr/bin/env bash

ZONE=europe-west1-b
SERVER_ARCHIVE=get_involved_server-1.0.tar.gz
INSTANCE_NAME=gi-server

gcloud compute copy-files ./dist/${SERVER_ARCHIVE} ${INSTANCE_NAME}:~/ --zone ${ZONE}

# upload client command example:
# gcloud compute copy-files ./../clients/web/dist/app.zip root@gi-server:/var/www/html/ --zone europe-west1-b

