# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CensusItem(scrapy.Item):
    '''Represent the census for a single facitily on a single 
    date.
    '''

    date = scrapy.Field()
    facility = scrapy.Field(serializer=str)
    adult_female = scrapy.Field(serializer=int)
    adult_male = scrapy.Field(serializer=int)
    emergency_room_trip_female = scrapy.Field(serializer=int)
    emergency_room_trip_male = scrapy.Field(serializer=int)
    furlough_female = scrapy.Field(serializer=int)
    furlough_male = scrapy.Field(serializer=int)
    in_out_female = scrapy.Field(serializer=int)
    in_out_male = scrapy.Field(serializer=int)
    juvenile_female = scrapy.Field(serializer=int)
    juvenile_male = scrapy.Field(serializer=int)
    open_ward_female = scrapy.Field(serializer=int)
    open_ward_male = scrapy.Field(serializer=int)
    total_count = scrapy.Field(serializer=int)
    worker_female = scrapy.Field(serializer=int)
    worker_male = scrapy.Field(serializer=int)
