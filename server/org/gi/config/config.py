__author__ = 'avishayb'
import json
import sys
_config = None
_loaded = False

DEFAULT_DB_URI = 'mongodb://localhost:27017/getinvolved'


def _load_config():
    global _config
    global _loaded
    if not _loaded:
        try:
            _loaded = True
            path = sys.modules[__name__].__file__
            if path.endswith('pyc'):
                path = path.replace('config.pyc', 'config.json')
            else:
                path = path.replace('config.py', 'config.json')
            with open(path) as data_file:
                _config = json.load(data_file)
        except Exception as e:
            print(str(e))


def get_db_uri():
    global _config
    _load_config()
    return _config['db_uri'] if _config and 'db_uri' in _config else DEFAULT_DB_URI
