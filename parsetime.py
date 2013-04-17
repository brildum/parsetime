import calendar, datetime, re
from dateutil import relativedelta

def parse_dt(value, tzinfo=None):
    if tzinfo is None:
        tzinfo = _utc
    match = _relative_re.match(value)
    if match:
        return _parse_relative(match, tzinfo)
    match = _datetime_re.match(value)
    if match:
        return _parse_datetime(match, tzinfo)
    match = _word_re.match(value)
    if match:
        return _parse_word(value, tzinfo)
    raise ValueError('Invalid time string {}'.format(value))

def parse_ts(value, tzinfo=None):
    return _timestamp(parse_dt(value, tzinfo))

class _utc_tzinfo(datetime.tzinfo):
    UTC = datetime.timedelta(0)
    def utcoffset(self, dt):
        return self.UTC
    def dst(self, dt):
        return self.UTC

_utc = _utc_tzinfo()

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

def _now(tzinfo):
    return datetime.datetime.now(tzinfo)

def _today(tzinfo):
    return _beginning_of_day(_now(tzinfo))

def _tomorrow(tzinfo):
    return _beginning_of_day(_now(tzinfo) + relativedelta.relativedelta(days=1))

def _yesterday(tzinfo):
    return _beginning_of_day(_now() + relativedelta.relativedelta(days=-1))

_valid_words = {
    'now': _now,
    'today': _today,
    'tomorrow': _tomorrow,
    'yesterday': _yesterday,
}

def _parse_relative(match, tzinfo):
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
    return _now(tzinfo) + delta

def _parse_datetime(match, tzinfo):
    kwargs = { 'tzinfo': tzinfo }
    kwargs['year'] = int(match.group(1))
    kwargs['month'] = int(match.group(2))
    kwargs['day'] = int(match.group(3))
    if match.group(4):
        kwargs['hour'] = int(match.group(5))
        kwargs['minute'] = int(match.group(6))
        kwargs['second'] = int(match.group(7))
    return datetime.datetime(**kwargs)

def _parse_word(value, tzinfo):
    if value not in _valid_words:
        raise ValueError("Invalid timestring {}".format(value))
    return _valid_words[value](tzinfo)

def _beginning_of_day(dt):
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

def _timestamp(dt):
    return int(calendar.timegm(dt.utctimetuple()))
