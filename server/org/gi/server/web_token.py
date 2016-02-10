import jwt
import time
from org.gi.config import config

ACCESS_TOKEN_TTL = 24 * 60 * 60


def generate_access_token(db_user):
    # Probably use a subset of user info - some fields will be required (fb_access_token?)
    user = {
        'user_name': db_user['user_name'],
        'email': db_user['email'],
        'role': db_user['role'],
        '_id': str(db_user['_id']),
        'facebook_id': db_user['facebook_id'] if 'facebook_id' in db_user else "",
        'facebook_access_token': db_user['facebook_access_token'] if 'facebook_access_token' in db_user else "",
    }

    encoded = jwt.encode(
            {
                "user": user,
                "timestamp": time.time()
            }, config.get('secret_key'))
    return encoded


def get_user_from_access_token(access_token):
    try:
        decoded = jwt.decode(access_token, config.get('secret_key'))
        if time.time() - decoded['timestamp'] < ACCESS_TOKEN_TTL:
            return decoded['user']
    except:
        return


class AccessTokenAuth:
    """Attaches HTTP Basic Authentication to the given Request object."""
    def __init__(self, access_token):
        self.access_token = access_token

    def __call__(self, r):
        r.headers['Authorization'] = self.access_token
        return r

