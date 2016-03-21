#!/usr/bin/env bash

#
# This one runs on the GCE instance
#

echo "Running remote..."
SERVER_ARCHIVE=get_involved_server-1.0.tar.gz

mv ${SERVER_ARCHIVE} ../getinvolved_dev
cd ../getinvolved_dev
sudo tar -zxvf ${SERVER_ARCHIVE}
cd get_involved_server-1.0
sudo python setup.py install
PID=$(ps -ef | grep org.gi.server.server | grep python | awk '{print $2}')
if [ ! -z "$PID" ]; then
    echo "Kill the server and wait until its down.."
    sudo kill ${PID}
    sleep 10
else
    echo "GI Server is not running.. no need to kill and wait."
fi

`sudo python -m org.gi.server.server --mode dev &`


