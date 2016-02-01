from setuptools import setup

setup(
    name='GI Server',
    version='1.0',
    long_description=__doc__,
    packages=['org.gi.config','org.gi.server'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask',
                      'flask_restful',
                      'pymongo',
                      'phonenumbers',
                      'pycountry']
)
