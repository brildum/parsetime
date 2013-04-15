parsetime
=========

This library provides a few related functions which allow parsing timestamps/datetimes
from strings.

There are a few classes of strings that parsetime handles, they are:

* Timestamps (``"2010-04-10"`` or ``"2010-04-10 12:30:15"``)
* Relative dates/times (``"7 days ago"`` or ``"10 minutes ago"``)

API
---

**parse_dt(s)**
    :s: ``string`` input

    Returns a UTC ``datetime`` representation of the input string.
    If the input string can not be parsed, it raises a ``ValueError``.

**parse_ts(s)**
    :s: ``string`` input

    Returns a UTC ``float`` timestamp representaion of the input string.
    If the input string can not be parsed, it raises a ``ValueError``.

Examples
--------
::

    >>> import parsetime
    >>> parsetime.parse_dt("7 days ago")
    datetime.datetime(2013, 4, 8, 0, 56, 25, 886358)
    >>> parsetime.parse_dt("3 hours ago")
    1365976689.0
