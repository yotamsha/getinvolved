from authomatic.providers import oauth2

config = {
    'fb': {
        'class_': oauth2.Facebook,

        'consumer_key': '1681765768739323',
        'consumer_secret': '081cc6e01a87f4282045991e600876e6',

        'scope': ['user_about_me', 'email']
    }
}
