from datetime import timezone, datetime


def format_euro(price):
    if price > 0:
        return '€{:,.2f}'.format(price)
    return '€0,00'


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def datetime_browser_format(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def start_of_year():
    return datetime(datetime.now().year, 1, 1, 0, 0, 0, 0)
