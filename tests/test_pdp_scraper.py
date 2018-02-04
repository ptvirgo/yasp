#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from datetime import date
from scrapy.http import TextResponse

from pdp_scraper.spiders.census_page import CensusPageSpider


class TestPDPScraper(unittest.TestCase):

    spider = CensusPageSpider()

    def test_dec_2017(self):
        '''Validate simple parsing of census from Dec, 2017'''

        response = self.sample('2017-12-31.html')
        items = list(self.spider.parse(response))
        self.assertEqual(len(items), 13, msg='incorrect facility count')

        asd = items[0]
        self.assertEqual(asd['facility'], 'ASD ASDCU')
        self.assertEqual(asd['date'], date(2017, 12, 26))

        self.assertEqual(asd['adult_male'], 124)
        self.assertEqual(asd['adult_female'], 1)
        self.assertIs(asd['juvenile_male'], None)
        self.assertIs(asd['juvenile_female'], None)

        pdp = items[12]
        self.assertEqual(pdp['facility'], 'PDP "In Facility" Count')
        self.assertEqual(pdp['adult_male'], 5707)
        self.assertEqual(pdp['adult_female'], 566)
        self.assertEqual(pdp['juvenile_male'], 27)
        self.assertEqual(pdp['juvenile_female'], 1)

    def test_facility_names(self):
        '''All facilty names should load correctly'''

        facilities = ['ASD ASDCU', 'ASD Cambria', 'ASD Cannery', 'ASD MOD 3',
                      'ASD WRP-UNIV. AVE', 'CFCF', 'DC-DETENTION CENTER',
                      'DC-PHSW', 'HOC', 'PICC', 'RCF', 'Weekenders',
                      'PDP "In Facility" Count']

        response = self.sample('2017-12-31.html')
        items = list(self.spider.parse(response))
        self.assertEqual(len(items), 13, msg='incorrect facility count')

        for i in range(13):
            self.assertEqual(items[i]['facility'], facilities[i])

    def test_field_values(self):
        '''Census attribute values should match the corresponding table
        cells.
        '''

        response = self.sample('field_check.html')
        items = list(self.spider.parse(response))
        self.assertEqual(len(items), 13, msg='incorrect facility count')

        picc = items[9]
        self.assertEqual(picc['facility'], 'PICC')
        self.assertEqual(picc['date'], date(2018, 1, 24))
        self.assertEqual(picc['adult_male'], 1)
        self.assertEqual(picc['adult_female'], 2)
        self.assertEqual(picc['juvenile_male'], 3)
        self.assertEqual(picc['juvenile_female'], 4)
        self.assertEqual(picc['in_out_male'], 5)
        self.assertEqual(picc['in_out_female'], 6)
        self.assertEqual(picc['worker_male'], 7)
        self.assertEqual(picc['worker_female'], 8)
        self.assertEqual(picc['furlough_male'], 9)
        self.assertEqual(picc['furlough_female'], 10)
        self.assertEqual(picc['open_ward_male'], 11)
        self.assertEqual(picc['open_ward_female'], 12)
        self.assertEqual(picc['emergency_room_trip_male'], 13)
        self.assertEqual(picc['emergency_room_trip_female'], 14)

    def test_clean_space(self):
        '''Make sure odd whitespace is cleared'''

        self.assertEqual(self.spider.clean_space('DC-PHSW'), 'DC-PHSW')
        self.assertEqual(
            self.spider.clean_space(' ASD \n  \tCambria\t\n  '),
            'ASD Cambria')

    def test_as_int(self):
        '''Make sure integers are handled'''

        self.assertEqual(self.spider.as_int(15), 15)
        self.assertEqual(self.spider.as_int("3"), 3)

        self.assertIs(self.spider.as_int(None), None)
        self.assertEqual(self.spider.as_int('  \n24}'), 24)
        self.assertIs(self.spider.as_int("#REF"), None)

    # Helpers

    def sample(self, filename):
        '''Create a sample TextResponse from the provided filename.
        Parameters:
        filename -- reference an html file as pulled from the PDP Census
                    page
        '''

        path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(path, 'pdp_samples', filename)

        with open(file_path, 'r') as f:
            response = TextResponse(
                'http://www.phila.gov/prisons/inmatesupport/Pages/Census.aspx',
                status=200, encoding='utf-8', body=f.read())

        return response


if __name__ == "__main__":
    unittest.main()
