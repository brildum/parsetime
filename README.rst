parsetime
=========

This library provides a few related functions which allow parsing timestamps/datetimes
from strings.

There are a few classes of strings that parsetime handles, they are:

* Timestamps (``"2010-04-10"`` or ``"2010-04-10 12:30:15"``)
* Relative dates/times (``"7 days ago"`` or ``"10 minutes ago"``)
* Specific keywords (``"now"``, ``"today"``, ``"tomorrow"``, or ``"yesterday"``)

API
---

**parse_dt(value[, *tzinfo=None*])**
    **value** ``string``
    **tzinfo** ``tzinfo``

    Returns ``datetime`` representation of the input value with ``tzinfo`` matching
    that of the ``tzinfo`` parameter. If ``tzinfo`` is ``None``, UTC is assumed.
    If the input can not be parsed, raises ``ValueError``.

**parse_ts(value[, *tzinfo=None*])**
    **value** ``string``
    **tzinfo** ``tzinfo``

    Returns a UTC ``int`` timestamp representation of the input value according
    to the ``tzinfo`` parameter specified. If ``tzinfo`` is ``None``, UTC is assumed.
    If the input can not be parsed, raises ``ValueError``.

Examples
--------
::

    >>> import parsetime
    >>> parsetime.parse_dt("7 days ago")
    datetime.datetime(2013, 4, 8, 0, 56, 25, 886358)
    >>> parsetime.parse_dt("2013-04-08 00:56::25")
    datetime.datetime(2013, 4, 8, 0, 56, 25, 0)
    >>> parsetime.parse_ts("3 hours ago")
    1365976689
