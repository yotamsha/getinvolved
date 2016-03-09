from datetime import datetime
from babel.dates import format_datetime

# Babel date & time guide
# http://babel.pocoo.org/en/latest/dates.html


def from_seconds_to_locale_date(seconds, locale='he'):
    _datetime = datetime.fromtimestamp(seconds)
    locale_datetime = format_datetime(_datetime, format='(MM/dd) E hh:mm a', locale=locale)
    return locale_datetime

