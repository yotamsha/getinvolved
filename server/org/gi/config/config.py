import os

__author__ = 'avishayb'
import json
import sys

_config = None
_loaded = False

DEFAULT_DB_URI = 'mongodb://localhost:27017/getinvolved'
CONFIG_FILE = '{}_config.json'


def _load_config():
    global _config
    global _loaded
    if not _loaded:
        try:
            _loaded = True
            path = sys.modules[__name__].__file__
            mode = os.environ['__MODE']
            if path.endswith('pyc'):
                path = path.replace('config.pyc', CONFIG_FILE.format(mode))
            else:
                path = path.replace('config.py', CONFIG_FILE.format(mode))
            with open(path) as data_file:
                print 'Loading config {}'.format(path)
                _config = json.load(data_file)
        except Exception as e:
            print(str(e))


def get_db_uri():
    global _config
    _load_config()
    return _config['db_uri'] if _config and 'db_uri' in _config else DEFAULT_DB_URI


def get(key):
    global _config
    _load_config()
    if _config and key in _config:
        return _config[key]
    else:
        raise Exception("No key {} present in {}".format(key, CONFIG_FILE))
