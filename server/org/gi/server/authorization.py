import os

from flask import request, Response, session
import hashlib
from functools import wraps
from org.gi.server import utils as u
from org.gi.server.db import db
from org.gi.server.web_token import get_user_from_access_token

__author__ = 'avishayb'

NONE = 'ROLE_NONE'
USER = 'ROLE_USER'
POWER_USER = 'ROLE_POWER_USER'
ADMIN = 'ROLE_ADMIN'

ROLES = {NONE: 0, USER: 1, POWER_USER: 2, ADMIN: 5}


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_current_user_role(*args) not in roles:
                return 'Not authorized', u.HTTP_UNAUTHORIZED
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def get_current_user_role(user_id):
    # TODO implement
    return ROLES.keys()[0]

# ------------------------------------------------------------------------------------


# mode = None


def hash_password(password):
    md5 = hashlib.md5()
    md5.update(password)
    return md5.hexdigest()


def check_auth(user_name, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    mode = os.environ['__MODE']
    if not mode:
        raise Exception('Failed to authenticate (mode is None)')
    if mode == 'dev':
        if not db:
            raise Exception('Failed to authenticate (db is None)')
        pwd_hash = hash_password(password)
        count = db.users.count(
            {'$and': [{'user_name': {'$eq': user_name}}, {'password': {'$eq': pwd_hash}}]}) == 1
        if not count:
            return user_name == 'admin' and password == 'admin'
        return count
    elif mode == 'production':
        if not db:
            raise Exception('Failed to authenticate (db is None)')
        pwd_hash = hash_password(password)
        return db.users.count(
            {'$and': [{'user_name': {'$eq': user_name}}, {'password': {'$eq': pwd_hash}}]}) == 1
    else:
        raise Exception('Unsupported mode: %s', mode)


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


def check_access_token(access_token):
    user = get_user_from_access_token(access_token)
    if user:
        session['user'] = user
        return True
    return False


def requires_access_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        if not access_token or not check_access_token(access_token):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


