#!/usr/bin/env python
# encoding: utf-8
"""
Unit tests for cit.py
"""
from __future__ import print_function, unicode_literals
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

    def test_parse_date_to_string_2(self):
        # Arrange
        date = "feb-03-2016"

        # Act
        ret = cit.validate_date(date)

        # Assert
        self.assertEqual(ret, "3 February 2016")

    def test_embolden_lc_lc_lc(self):
        # Arrange
        word = "this"
        quote = "make this and this bold"

        # Act
        ret = cit.embolden(word, quote)

        # Assert
        self.assertEqual(ret, "make <b>this</b> and <b>this</b> bold")

    def test_embolden_uc_uc_uc(self):
        # Arrange
        word = "THIS"
        quote = "make THIS and THIS bold"

        # Act
        ret = cit.embolden(word, quote)

        # Assert
        self.assertEqual(ret, "make <b>THIS</b> and <b>THIS</b> bold")

    def test_embolden_lc_lc_uc(self):
        # Arrange
        word = "this"
        quote = "make this and THIS bold"

        # Act
        ret = cit.embolden(word, quote)

        # Assert
        self.assertEqual(ret, "make <b>this</b> and <b>THIS</b> bold")

    def test_embolden_mixed_cases(self):
        # Arrange
        word = "THis"
        quote = "make thIS and ThiS bold"

        # Act
        ret = cit.embolden(word, quote)

        # Assert
        self.assertEqual(ret, "make <b>thIS</b> and <b>ThiS</b> bold")

    def test_embolden_substring(self):
        # Arrange
        word = "thing"
        quote = "make things bold"

        # Act
        ret = cit.embolden(word, quote)

        # Assert
        self.assertEqual(ret, "make <b>thing</b>s bold")

    def test_embolden_phrase(self):
        # Arrange
        word = "this phrase"
        quote = "Embolden this phrase and 'This Phrase' and \"THIS PHRASE\"."

        # Act
        ret = cit.embolden(word, quote)

        # Assert
        self.assertEqual(ret, "Embolden <b>this phrase</b> and "
                              "'<b>This Phrase</b>' and "
                              "\"<b>THIS PHRASE</b>\".")

    def test_source_from_url_washingtonpost(self):
        # Arrange
        url = ("https://www.washingtonpost.com/news/checkpoint/wp/2016/01/19/"
               "more-u-s-military-drones-are-crashing-than-ever-as-new-"
               "problems-emerge/")

        # Act
        ret = cit.source_from_url(url)

        # Assert
        self.assertEqual(ret, "Washington Post")

    def test_source_from_url_twitter(self):
        # Arrange
        url = ("https://twitter.com/Chris_Boardman/status/691588823419977728")

        # Act
        ret = cit.source_from_url(url)

        # Assert
        self.assertEqual(ret, "@Chris_Boardman")

    def test_source_from_url_generic_with_www_and_the(self):
        # Arrange
        url = ("http://www.theguardian.com/science/2016/jan/20/"
               "ninth-planet-solar-system-edge-discovery-pluto")

        # Act
        ret = cit.source_from_url(url)

        # Assert
        self.assertEqual(ret, "The Guardian")

    def test_source_from_url_generic_no_www(self):
        # Arrange
        url = ("http://yle.fi/uutiset/officials_see_signs_of_hybrid_warfare_in"
               "_migrant_crisis/8672574")

        # Act
        ret = cit.source_from_url(url)

        # Assert
        self.assertEqual(ret, "Yle")

    def test_date_from_url_yyyy_mm_dd(self):
        # Arrange
        url = ("https://www.washingtonpost.com/news/checkpoint/wp/2016/01/19/"
               "more-u-s-military-drones-are-crashing-than-ever-as-new-"
               "problems-emerge/")

        # Act
        ret = cit.date_from_url(url)

        # Assert
        self.assertEqual(ret, "19 January 2016")

    def test_date_from_url_yyyy_mon_dd(self):
        # Arrange
        url = ("http://www.theguardian.com/science/2016/jan/20/"
               "ninth-planet-solar-system-edge-discovery-pluto")

        # Act
        ret = cit.date_from_url(url)

        # Assert
        self.assertEqual(ret, "20 January 2016")


if __name__ == '__main__':
    unittest.main()

# End of file
