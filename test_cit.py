#!/usr/bin/env python
# encoding: utf-8
"""
Unit tests for cit.py
"""
from __future__ import print_function, unicode_literals
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import datetime

import cit


class TestIt(unittest.TestCase):

    def test_parse_now_or_past_invalid(self):
        # Arrange
        date = "not a date"

        # Act / Assert
        self.assertRaises(ValueError, lambda: cit.parse_now_or_past(date))

    def test_parse_now_or_past_earlier_this_year(self):
        """Assumes this isn't run on 1st January..."""
        # Arrange
        date = "1 January"
        now = datetime.datetime.now()

        # Act
        ret = cit.parse_now_or_past(date)

        # Assert
        self.assertEqual(ret.day, 1)
        self.assertEqual(ret.month, 1)
        self.assertEqual(ret.year, now.year)

    def test_parse_now_or_past_last_year(self):
        """Assumes this isn't run on 31st December..."""
        # Arrange
        date = "31 December"
        now = datetime.datetime.now()

        # Act
        ret = cit.parse_now_or_past(date)

        # Assert
        self.assertEqual(ret.day, 31)
        self.assertEqual(ret.month, 12)
        self.assertEqual(ret.year, now.year-1)

    def test_parse_now_or_past_today(self):
        # Arrange
        now = datetime.datetime.now()
        date = now.strftime("%d %B")  # e.g. "11 January"

        # Act
        ret = cit.parse_now_or_past(date)

        # Assert
        self.assertEqual(ret.day, now.day)
        self.assertEqual(ret.month, now.month)
        self.assertEqual(ret.year, now.year)

    def test_parse_date_to_string(self):
        # Arrange
        date = "11 Jan 2016"

        # Act
        ret = cit.validate_date(date)

        # Assert
        self.assertEqual(ret, "11 January 2016")


if __name__ == '__main__':
    unittest.main()

# End of file
