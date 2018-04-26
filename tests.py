#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Sölvi Páll Ásgeirsson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import unittest

from datetime import datetime, timedelta
from icelandic_holidays import (
    is_holiday, is_businessday, is_bankday, holiday_names, get_holiday_name
)
from icelandic_holidays.api import __easter_sunday as easter_sunday

class HolidayTests(unittest.TestCase):
    def setUp(self):
        # Holidays stolen from http://www.almanak.hi.is/
        self.holidays = {
            holiday_names.JANUARY_1ST: datetime(2013, 1, 1),
            holiday_names.HOLY_THURSDAY: datetime(2013, 3, 28),
            holiday_names.GOOD_FRIDAY: datetime(2013, 3, 29),
            holiday_names.EASTER_SUNDAY: datetime(2013, 3, 31),
            holiday_names.EASTER_MONDAY: datetime(2013, 4, 1),
            holiday_names.FIRST_DAY_OF_SUMMER: datetime(2013, 4, 25),
            holiday_names.MAY_1ST: datetime(2013, 5, 1),
            holiday_names.ASCENSION_OF_JESUS: datetime(2013, 5, 9),
            holiday_names.WHIT_MONDAY: datetime(2013, 5, 20),
            holiday_names.JUNE_17TH: datetime(2013, 6, 17),
            holiday_names.MERCHANT_HOLIDAY: datetime(2013, 8, 5),
            holiday_names.CHRISTMAST_DAY: datetime(2013, 12, 25),
            holiday_names.SECOND_DAY_OF_CHRISTMAS: datetime(2013, 12, 26)
        }

        self.businessdays = [
            datetime(2013, 1, 8),
            datetime(2013, 2, 14),
            datetime(2013, 2, 28),
            datetime(2013, 4, 18) ]

        self.weekend_days = [
            datetime(2013, 1, 2),
            datetime(2013, 2, 7),
            datetime(2013, 2, 14),
            datetime(2013, 2, 21) ]

        self.easter_sundays = [
            datetime(1736, 4, 1),
            datetime(1709, 3, 31),
            datetime(1734, 4, 25),
            datetime(1784, 4, 11),
            datetime(1710, 4, 20),
            datetime(2008, 3, 23),
            datetime(2215, 4, 16),
            datetime(2240, 4, 12),
            datetime(2292, 4, 10) ]

    def test_holidays(self):
        for day in self.holidays.values():
            self.assertTrue(is_holiday(day), msg="%s wasn't holiday" % day)

        for day in self.businessdays:
            self.assertFalse(is_holiday(day),
                             msg="%s was a holiday, shouldn't have been" % day)

    def test_businessdays(self):
        for day in self.businessdays:
            self.assertTrue(is_businessday(day), msg="%s wasn't a business day" % day)

        for day in self.holidays.values():
            self.assertFalse(is_businessday(day),
                             msg="%s was a business day, shouldn't have been" % day)

    def test_easter_sunday(self):
        for sunday in self.easter_sundays:
            self.assertTrue(easter_sunday(sunday),
                            msg="%s wasn't an easter sunday" % sunday)
        # Ensure that there's only a single easter sunday pr. year
        for year in range(1800, 2200):
            start_of_year = datetime(year, 1, 1)
            num_easter = 0
            for i in range(1, 365):
                if easter_sunday(start_of_year + timedelta(days=i)):
                    num_easter += 1

            self.assertEqual(num_easter, 1)

    def test_bankdays(self):
        self.assertTrue(is_bankday(datetime(2013, 12, 31)))
        self.assertTrue(is_bankday(datetime(2014, 12, 31)))
        self.assertTrue(is_bankday(datetime(2015, 12, 31)))
        self.assertFalse(is_bankday(datetime(2016, 12, 31))) # Dec. 31st is a saturday

    def test_holiday_names(self):
        for name, day in self.holidays.items():
            self.assertEqual(
                get_holiday_name(day),
                name,
                msg="%s expected to be %s" % (day, name)
            )


if __name__ == "__main__":
    unittest.main()
