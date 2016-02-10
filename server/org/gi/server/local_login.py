from flask import request, Blueprint, session
from org.gi.server.authorization import requires_auth, requires_user_password
from org.gi.server.db import db
from org.gi.server.web_token import generate_access_token


local_login_bp = Blueprint('local_login_bp', __name__)


@local_login_bp.route('/login', methods=['GET', 'POST'])
@requires_user_password
def login():
    username = request.authorization.username
    user = db.users.find_one({'user_name': username})
    if user:
        return generate_access_token(user)
    raise Exception('No user with username {} exists'.format(request.authorization.username))
