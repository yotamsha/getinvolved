__author__ = 'avishayb'
from functools import wraps
from org.gi.server import utils as u


USER = 'ROLE_USER'
POWER_USER = 'ROLE_POWER_USER'
ADMIN = 'ROLE_ADMIN'

ROLES = {USER: 0, POWER_USER: 1, ADMIN: 3}


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
    #TODO implement
    return ROLES.keys()[0]