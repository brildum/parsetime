import datetime, sys, unittest
import mock
from dateutil import relativedelta
import parsetime

def suite():
    loader = unittest.TestLoader()
    return loader.loadTestsFromModule(sys.modules[__name__])

class ParseDT_RelativeTests(unittest.TestCase):
    NOW = datetime.datetime(2013, 1, 1, 12, 0, 0, 0, None)

    def setUp(self):
        self._old_now = parsetime._now
        parsetime._now = mock.Mock(parsetime._now)
        parsetime._now.return_value = self.NOW

    def tearDown(self):
        parsetime._now = self._old_now

    def test_7_days(self):
        target = self._relative(days=7)
        self.assertEqual(parsetime.parse_dt("7 days"), target)

    def test_7_days_ago(self):
        target = self._relative(days=-7)
        self.assertEqual(parsetime.parse_dt("7 days ago"), target)

    def test_10_minutes(self):
        target = self._relative(minutes=10)
        self.assertEqual(parsetime.parse_dt("10 minutes"), target)

    def test_10_minutes_ago(self):
        target = self._relative(minutes=-10)
        self.assertEqual(parsetime.parse_dt("10 minutes ago"), target)

    def test_1_hour(self):
        target = self._relative(hours=1)
        self.assertEqual(parsetime.parse_dt("1 hour"), target)

    def test_1_hour_ago(self):
        target = self._relative(hours=-1)
        self.assertEqual(parsetime.parse_dt("1 hour ago"), target)

    def test_1_minute(self):
        target = self._relative(minutes=1)
        self.assertEqual(parsetime.parse_dt("1 minute"), target)

    def test_1_minute_ago(self):
        target = self._relative(minutes=-1)
        self.assertEqual(parsetime.parse_dt("1 minute ago"), target)

    def test_3_weeks_ago(self):
        target = self._relative(weeks=-3)
        self.assertEqual(parsetime.parse_dt("3 weeks ago"), target)

    def test_15_months_ago(self):
        target = self._relative(months=-15)
        self.assertEqual(parsetime.parse_dt("15 months ago"), target)

    def test_80_years_ago(self):
        target = self._relative(years=-80)
        self.assertEqual(parsetime.parse_dt("80 years ago"), target)

    def _relative(self, **kwargs):
        target = parsetime._now() + relativedelta.relativedelta(**kwargs)
        return target

class ParseDT_InvalidRelativeTests(unittest.TestCase):
    def test_7_lightyears_ago(self):
        self.assertRaises(ValueError, parsetime.parse_dt, "7 lightyears ago")

    def test_7_days_from_now(self):
        self.assertRaises(ValueError, parsetime.parse_dt, "7 days from now")

    def test_days_ago(self):
        self.assertRaises(ValueError, parsetime.parse_dt, "days ago")

    def test_float_days_ago(self):
        self.assertRaises(ValueError, parsetime.parse_dt, "13.4 days ago")

    def test_extra_whitespace(self):
        self.assertRaises(ValueError, parsetime.parse_dt, " 7 days ago ")

class ParseDT_TimestampTests(unittest.TestCase):
    def test_2013_10_10(self):
        target = datetime.datetime(2013, 10, 10, tzinfo=None)
        self.assertEqual(parsetime.parse_dt("2013-10-10"), target)

    def test_2013_10_10_203015(self):
        target = datetime.datetime(2013, 10, 10, 20, 30, 15, tzinfo=None)
        self.assertEqual(parsetime.parse_dt("2013-10-10 20:30:15"), target)

class ParseDT_InvalidTimestampTests(unittest.TestCase):
    def test_2013_10_10_10(self):
        self.assertRaises(ValueError, parsetime.parse_dt, "2013-10-10 10")

    def test_2013_90_90(self):
        self.assertRaises(ValueError, parsetime.parse_dt, "2013-90-90")

    def test_2013(self):
        self.assertRaises(ValueError, parsetime.parse_dt, "2013")

    def test_extra_whitespace(self):
        self.assertRaises(ValueError, parsetime.parse_dt, " 2013-10-10")

class ParseDT_WordTests(unittest.TestCase):
    NOW = datetime.datetime(2013, 1, 1, 12, 0, 0, 0, None)

    def setUp(self):
        self._old_now = parsetime._now
        parsetime._now = mock.Mock(parsetime._now)
        parsetime._now.return_value = self.NOW

    def tearDown(self):
        parsetime._now = self._old_now

    def test_today(self):
        target = datetime.datetime(2013, 1, 1, 0, 0, 0, 0, None)
        self.assertEqual(parsetime.parse_dt("today"), target)

    def test_tomorrow(self):
        target = datetime.datetime(2013, 1, 2, 0, 0, 0, 0, None)
        self.assertEqual(parsetime.parse_dt("tomorrow"), target)

    def test_yesterday(self):
        target = datetime.datetime(2012, 12, 31, 0, 0, 0, 0, None)
        self.assertEqual(parsetime.parse_dt("yesterday"), target)

class ParseDT_InvalidWordTests(unittest.TestCase):
    def test_extra_whitespace(self):
        self.assertRaises(ValueError, parsetime.parse_dt, " today ")

    def test_lastweek(self):
        self.assertRaises(ValueError, parsetime.parse_dt, "lastweek")
