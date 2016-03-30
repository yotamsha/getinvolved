__author__ = 'avishayb'

LENGTH_CONSTRAINTS = {
    'user': {'password': (8, 12), 'first_name': (2, 22), 'last_name': (2, 22)}
}


# ----------------------

PASSWORD_MIN = 8
PASSWORD_MAX = 12

FIRST_NAME_MIN = 2
FIRST_NAME_MAX = 22

LAST_NAME_MIN = 2
LAST_NAME_MAX = 22

USER_NAME_MIN = 2
USER_NAME_MAX = 22

TITLE_NAME_MIN = 2
TITLE_NAME_MAX = 22

DESCRIPTION_NAME_MIN = 2
DESCRIPTION_NAME_MAX = 22

FB_TOKEN_MIN_LENGTH = 10
FB_ID_MIN_LENGTH = 8
FB_ID_MAX_LENGTH = 40

MAX_DUE_DATE_HOURS = 24

TASK_MIN_DURATION_MINUTES = 60
TASK_MAX_DURATION_MINUTES = 60 * 24

ONE_DAY_SECONDS = 60 * 60 * 24
MIN_DUE_DATE_SECONDS = ONE_DAY_SECONDS
MAX_DUE_DATE_SECONDS = ONE_DAY_SECONDS * 90

TASK_DESCRIPTION_MIN = 10
TASK_DESCRIPTION_MAX = 50

TASK_TITLE_MIN = 8
TASK_TITLE_MAX = 25

# {
#     'resource': 'task',
#     'fields': [{'name': 'description', 'min_len': 10, 'max_len': 50},
#                {'name': 'title', 'min_len': 8, 'max_len': 25},
#                {'name': 'STREET_NAME_MIN', 'min_len': 2, 'max_len': 22},
#                {'name': 'user_name', 'min_len': 2, 'max_len': 22}]
# }


