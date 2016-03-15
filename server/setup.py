import os
from setuptools import setup


for dirName, subdirList, fileList in os.walk('org/gi/server/service/templates/data'):
    print('Found directory: %s' % dirName)
    for fname in fileList:
        print('\t%s' % fname)



setup(
    name='get_involved_server',
    version='1.0',
    long_description=__doc__,
    packages=['org.gi.config',
              'org.gi.server',
              'org.gi.server.api',
              'org.gi.server.model',
              'org.gi.server.service.notification',
              'org.gi.server.service.templates',
              'org.gi.server.validation',
              'org.gi.server.validation.task',
              'org.gi.server.model'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask',
                      'flask_restful',
                      'flask_oauth',
                      'PyJWT',
                      'pymongo',
                      'phonenumbers',
                      'requests',
                      'pycountry',
                      'flask-cors',
                      'babel', 'mock']
)