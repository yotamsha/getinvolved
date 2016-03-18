from setuptools import setup, find_packages



# packages=['org.gi.config',
#           'org.gi.server',
#           'org.gi.server.api',
#           'org.gi.server.model',
#           'org.gi.server.service.notification',
#           'org.gi.server.service.templates',
#           'org.gi.server.validation',
#           'org.gi.server.validation.task',
#           'org.gi.server.model'],


setup(
    name='get_involved_server',
    version='1.0',
    long_description=__doc__,
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=['flask',
                      'flask_restful',
                      'flask_oauth',
                      'PyJWT',
                      'pymongo',
                      'phonenumbers',
                      'requests',
                      'pycountry',
                      'flask-cors',
                      'babel',
                      'mock==1.0.1']
)