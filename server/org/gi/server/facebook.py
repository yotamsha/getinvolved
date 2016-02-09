from flask import request, url_for, session, Blueprint
from flask_oauth import OAuth

from org.gi.config import config
from org.gi.server.authorization import ROLES, USER
from org.gi.server.db import db
from org.gi.server.web_token import generate_access_token, get_user_from_access_token


__author__ = 'bazza'

facebook_bp = Blueprint('facebook_bp', __name__)
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=config.get('fb_app_id'),
    consumer_secret=config.get('fb_app_secret'),
    request_token_params={'scope': 'email'}
)


@facebook_bp.route('/login/fb')
def login_fb():
    return facebook.authorize(callback=url_for('facebook_bp.facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@facebook_bp.route('/login/fb/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    session['fb_access_token'] = (resp['access_token'], '')

    me = facebook.get('/me?fields=id,email,first_name,last_name')
    user = {
        'user_name': me.data['email'],
        'first_name': me.data['first_name'],
        'last_name': me.data['last_name'],
        'email': me.data['email'],
        'role': ROLES[USER],
        'facebook_id': me.data['id'],
        'facebook_access_token': (resp['access_token'], ''),
    }

    db_user = db.users.find_one({'facebook_id': user['facebook_id']})
    if not db_user:
        db_user = db.users.insert_one(user)

    access_token = generate_access_token(db_user)
    return access_token


# Internally used whenever facebook.get(..) is called
@facebook.tokengetter
def get_facebook_oauth_token():
    if 'fb_access_token' in session:
        fb_token = session['fb_access_token']
        if fb_token:
            return fb_token
    access_token = request.headers.get('Authorization')
    if access_token:
        user = get_user_from_access_token(access_token)
        return user['facebook_access_token']