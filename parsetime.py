import calendar, datetime, re
from dateutil import relativedelta

def parse_dt(s):
    match = _relative_re.match(s)
    if match:
        return _parse_relative(match)
    match = _datetime_re.match(s)
    if match:
        return _parse_datetime(match)
    match = _word_re.match(s)
    if match:
        return _parse_word(s)
    raise ValueError('Invalid time string {}'.format(s))

def parse_ts(s):
    return _timestamp(parse_dt(s))

_word_re = re.compile(r'^\w+$')
_relative_re = re.compile(r'^(\d+)\s+(\w+)(\s+(\w+))?$')
_datetime_re = re.compile(r'^(\d{4})-(\d{2})-(\d{2})( (\d{2}):(\d{2}):(\d{2}))?$')

_valid_units = {
    'second': 'seconds',
    'seconds': 'seconds',
    'minute': 'minutes',
    'minutes': 'minutes',
    'hour': 'hours',
    'hours': 'hours',
    'day': 'days',
    'days': 'days',
    'week': 'weeks',
    'weeks': 'weeks',
    'month': 'months',
    'months': 'months',
    'year': 'years',
    'years': 'years',
}

def _now():
    return datetime.datetime.utcnow()

def _today():
    return _beginning_of_day(_now())

def _tomorrow():
    return _beginning_of_day(_now() + relativedelta.relativedelta(days=1))

def _yesterday():
    return _beginning_of_day(_now() + relativedelta.relativedelta(days=-1))

_valid_words = {
    'now': _now,
    'today': _today,
    'tomorrow': _tomorrow,
    'yesterday': _yesterday,
}

def _parse_relative(match):
    value = int(match.group(1))
    unit = match.group(2)
    if unit not in _valid_units:
        raise ValueError('Invalid unit: {}'.format(unit))
    direction = match.group(4)
    if direction is not None and direction != 'ago':
        raise ValueError('Invalid string {}'.format(direction))
    value_mult = 1 if direction is None else -1
    kwargs = { _valid_units[unit]: value * value_mult }
    delta = relativedelta.relativedelta(**kwargs)
    return _now() + delta

def _parse_datetime(match):
    kwargs = { 'tzinfo': None }
    kwargs['year'] = int(match.group(1))
    kwargs['month'] = int(match.group(2))
    kwargs['day'] = int(match.group(3))
    if match.group(4):
        kwargs['hour'] = int(match.group(5))
        kwargs['minute'] = int(match.group(6))
        kwargs['second'] = int(match.group(7))
    return datetime.datetime(**kwargs)

def _parse_word(s):
    if s not in _valid_words:
        raise ValueError("Invalid timestring {}".format(s))
    return _valid_words[s]()

def _beginning_of_day(dt):
    return datetime.datetime(dt.year, dt.month, dt.day, 0, 0, 0, 0, None)

def _timestamp(dt):
    return float(calendar.timegm(dt.timetuple()))
