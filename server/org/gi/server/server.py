import os

from flask import Flask
from flask_restful import Api

from org.gi.config import config
from org.gi.server import utils as u

from org.gi.server.static import static_bp
from org.gi.server.facebook import facebook_bp
from org.gi.server.local_login import local_login_bp

from org.gi.server.model.case import Case, CaseList
from org.gi.server.model.user import User, UserList


__author__ = 'avishayb'

app = Flask(__name__, static_url_path='')
app.register_blueprint(static_bp)
app.register_blueprint(facebook_bp)
app.register_blueprint(local_login_bp)
app.secret_key = config.get('secret_key')
api = Api(app)


api.add_resource(UserList, '/api/users')
api.add_resource(CaseList, '/api/cases')

api.add_resource(User, '/api/users/<string:user_id>', '/api/users')
api.add_resource(Case, '/api/cases/<string:case_id>', '/api/cases')


if __name__ == '__main__':
    mode = os.environ['__MODE']
    print('---------------------------------------------')
    print('GI server starts under %s mode' % mode)
    print('---------------------------------------------')
    app.run(debug=False)


@app.route('/api/ping')
def ping():
    return 'Pong', u.HTTP_OK