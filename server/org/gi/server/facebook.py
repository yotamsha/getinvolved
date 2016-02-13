import json

from flask import request, url_for, session, Blueprint, jsonify, Response
from flask_oauth import OAuth

from org.gi.config import config
from org.gi.server.authorization import USER
from org.gi.server.db import db
from org.gi.server.web_token import generate_access_token, get_user_from_access_token
import org.gi.server.utils as util
import org.gi.server.validations as valid

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

    return facebook_token((resp['access_token'], ''))


@facebook_bp.route('/login/fb_token/<fb_token>', methods=['GET'])
def facebook_token(fb_token):
    faults = []
    if not fb_token:
        return 'No access token supplied', util.HTTP_BAD_INPUT

    session['fb_access_token'] = fb_token
    fb_resp = facebook.get('/me?fields=id,email,first_name,last_name')
    if not fb_resp.status == util.HTTP_OK:
        return fb_resp.data['error']['message'], fb_resp.status

    req_fields = ['email', 'first_name', 'last_name', 'id']
    for req_field in req_fields:
        if not req_field in fb_resp.data:
            faults.append('Missing field {} in fb response'.format(req_field))

    if faults:
        faults.append('Could not retrieve all required user information from facebook')
        return create_error_response(faults)

    user = {
        'user_name': fb_resp.data['email'],
        'first_name': fb_resp.data['first_name'],
        'last_name': fb_resp.data['last_name'],
        'email': fb_resp.data['email'],
        'role': USER,
        'facebook_id': fb_resp.data['id'],
        'facebook_access_token': fb_token
    }

    valid.user_post_validate(user, faults)
    if not faults:
        db_user = db.users.find_one({'facebook_id': user['facebook_id']})
        if not db_user:
            try:
                if db.users.find_one({'email': user['email']}):
                    faults.append('A user already exists with the email: {}'.format(user['email']))
                    return create_error_response(faults)
                result = db.users.insert_one(user)
                db_user = db.users.find_one({'_id': util.to_object_id(result.inserted_id)})
            except Exception as e:
                print e
                db_user = {}
            if not db_user:
                return 'Failed to insert user to db', util.HTTP_BAD_INPUT

        access_token = generate_access_token(db_user)
        return access_token
    else:
        faults.append('Could not retrieve all required user information from facebook')
        return create_error_response(faults)


# Internally used whenever facebook.get(..) is called
@facebook.tokengetter
def get_facebook_oauth_token():
    secret = config.get('fb_app_secret')
    if 'fb_access_token' in session:
        fb_token = session['fb_access_token']
        if fb_token:
            return fb_token, secret
    access_token = request.headers.get('Authorization')
    if access_token:
        user = get_user_from_access_token(access_token)
        return user['facebook_access_token'], secret


def create_error_response(faults):
    resp = Response(json.dumps(faults), status=util.HTTP_BAD_INPUT, mimetype=util.MIME_JSON)
    return resp