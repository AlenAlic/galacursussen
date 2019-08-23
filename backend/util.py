from datetime import timezone, datetime
from backend.values import DATETIME_FORMAT
from random import choice
import string


def format_euro(price):
    if price > 0:
        return '€{:,.2f}'.format(price)
    return '€0,00'


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def datetime_browser_format(dt):
    return dt.strftime(DATETIME_FORMAT)


def start_of_year():
    return datetime(datetime.now().year, 1, 1, 0, 0, 0, 0)


def is_float(s):
    try:
        int(s)
        return True
    except (ValueError, TypeError):
        return False


def auth_token():
    allowed_chars = string.ascii_letters + '0123456789'
    return ''.join([choice(allowed_chars) for _ in range(128)])
