# -*- coding: utf-8 -*-

import re
import scrapy

from dateutil import parser

from ..items import CensusItem

class CensusPageSpider(scrapy.Spider):
    name = 'census_page'
    allowed_domains = ['http://www.phila.gov']
    start_urls = ['http://http://www.phila.gov/prisons/inmatesupport/Pages/Census.aspx']

    facilities = ['ASD ASDCU', 'ASD Cambria', 'ASD Cannery', 'ASD MOD 3',
                  'ASD WRP-UNIV. AVE', 'CFCF', 'DC-DETENTION CENTER', 'DC-PHSW',
                  'HOC', 'PICC', 'RCF', 'Weekenders', 'PDP "In Facility" Count'
                 ]

    def parse(self, response):

        named_row = '''//div[contains(@id,'Census_')]/table/tr/td''' + \
                    '''[contains(normalize-space(text()),'%s')]/parent::tr/td'''

        date_row = response.xpath(named_row % ('CENSUS FOR',))

        if date_row is not None:

            date_text = self.clean_space(date_row[1].xpath('text()').extract_first())
            
            try:
                dt = parser.parse(date_text).date()
            except:
                dt = None
        else:
            dt = None

        for facility_name in self.facilities:
            data = response.xpath(named_row % (facility_name,))
            census = CensusItem(
                facility=self.clean_space(data[0].xpath('text()').extract_first()),
                date=dt)

            ordered_fields = ['adult_male',
                              'adult_female',
                              'juvenile_male',
                              'juvenile_female',
                              'in_out_male',
                              'in_out_female',
                              'worker_male',
                              'worker_female',
                              'furlough_male',
                              'furlough_female', 
                              'open_ward_male', 
                              'open_ward_female', 
                              'emergency_room_trip_male', 
                              'emergency_room_trip_female' 
                             ]

            for i in range(len(ordered_fields)):
                census[ordered_fields[i]] = self.as_int(
                    data[i + 1].xpath('text()').extract_first())

            yield census   

    # Helpers

    @staticmethod
    def clean_space(text):
        return re.sub("[\s]+", " ", text.strip())


    @staticmethod
    def as_int(text):

        if text is None:
            return

        if type(text) is int:
            return text


        numbers = re.sub("[^\d]", "", text)

        try:
            number = int(numbers)
        except:
            number = None

        return number
