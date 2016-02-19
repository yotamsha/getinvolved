import os
import sys

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from org.gi.config import config
from org.gi.server import utils as u
from org.gi.server.service.scheduler import get_scheduler
from org.gi.server.api.case import Case, CaseList
from org.gi.server.api.user import User, UserList
from org.gi.server.facebook import facebook_bp
from org.gi.server.local_login import local_login_bp
from org.gi.server.static import static_bp


__author__ = 'avishayb'

app = Flask(__name__, static_url_path='')
CORS(app)
app.register_blueprint(static_bp)
app.register_blueprint(facebook_bp)
app.register_blueprint(local_login_bp)
app.secret_key = config.get('secret_key')


def start_notification_loop():
    """
    Start running the notification background thread
    :return:
    """
    from datetime import datetime
    def _notify(_data):
        if mode == 'dev':
            print('%s  > Notifier runs under dev mode...' % str(datetime.now()))
        elif mode == 'prod':
            #TODO implement the real notification logic see #194
            pass
    interval = 10 #TODO read from config
    scheduler, stop = get_scheduler(interval, _notify, None)
    scheduler.start()
    return scheduler, stop


@app.route('/api/ping')
def ping():
    return 'Pong', u.HTTP_OK


api = Api(app)

api.add_resource(UserList, '/api/users')
api.add_resource(CaseList, '/api/cases')

api.add_resource(User, '/api/users/<string:user_id>', '/api/users')
api.add_resource(Case, '/api/cases/<string:case_id>', '/api/cases')

if __name__ == '__main__':
    if sys.version_info[0] != 2 or sys.version_info[1] != 7:
        print('Oops...GI Server runs on python 2.7 only. Current Python version is %d.%d' % (
        sys.version_info[0], sys.version_info[1]))
        sys.exit(-1)
    mode = os.environ['__MODE']
    print('------------------------------------------------------------------------------------')
    print('GI server starts under %s mode. Python version is %d.%d.%d' % (
    mode, sys.version_info[0], sys.version_info[1], sys.version_info[2]))
    print('------------------------------------------------------------------------------------')
    start_notification_loop()
    app.run(debug=False)


