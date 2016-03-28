#
# run on remote box
#
ARCHIVE=get_involved_client.tar.gz
APACHE_ROOT=/var/www/html

sudo mv ${ARCHIVE} ${APACHE_ROOT}
echo $?
cd ${APACHE_ROOT}
echo $?
sudo tar -zxvf ${ARCHIVE}
echo $?
sudo cp -r ./app/* .
echo $?
sudo rm -rf ./app
echo $?
sudo rm -rf ${ARCHIVE}
echo $?
