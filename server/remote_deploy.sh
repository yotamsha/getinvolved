#!/usr/bin/env bash

#
# This one runs on the GCE instance
#

echo "Running remote..."
SERVER_ARCHIVE=get_involved_server-1.0.tar.gz

PID=$(ps -ef | grep org.gi.server.server | grep python | awk '{print $2}')
if [ ! -z "$PID" ]; then
    echo "Kill the server and wait until its down.."
    sudo kill ${PID}
    sleep 10
else
    echo "GI Server is not running.. no need to kill and wait."
fi
sudo rm -rf /usr/local/lib/python2.7/dist-packages/get_involved_server-1.0-py2.7.egg
echo $?
sudo mv ${SERVER_ARCHIVE} ../getinvolved_dev
echo $?
cd ../getinvolved_dev
echo $?
sudo rm -rf get_involved_server-1.0
echo $?
sudo tar -zxvf ${SERVER_ARCHIVE}
echo $?
cd get_involved_server-1.0
echo $?
sudo python setup.py install
echo $?


`sudo python -m org.gi.server.server --mode dev &`


