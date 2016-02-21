import pymongo
from pymongo import IndexModel

from org.gi.config import config


def handle_constraints():
    # user indexes
    email_index = IndexModel('email', name='email_index', unique=True)
    username_index = IndexModel('user_name', name='user_name_index', unique=True)
    phone_number_index = IndexModel(
        [("phone_number.number", pymongo.ASCENDING),
         ("phone_number.country_code", pymongo.ASCENDING)],
        name='phone_number_index', unique=True, sparse=True)

    # case indexes
    geo_location_index = IndexModel([('location.geo_location', pymongo.GEOSPHERE)],
                                    name='case_geo_index',
                                    unique=False,
                                    spare=True)

    db.users.create_indexes([email_index, phone_number_index, username_index])
    db.cases.create_indexes([geo_location_index])


mongo = pymongo.MongoClient(config.get_db_uri())
db = mongo.get_default_database()
handle_constraints()
