from setuptools import setup, find_packages

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