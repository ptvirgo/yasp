# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem

from census import Census, Facility

from .settings import CENSUS_DB


class CensusPipeline(object):

    engine = create_engine(CENSUS_DB)
    Session = sessionmaker(bind=engine)
    session = Session()

    def __del__(self):
        '''Close the database session'''
        self.session.close()

    def process_item(self, item, spider):
        '''Save Census items to the CENSUS_DB'''

        if self.census_exists(item['facility'], item['date']):
            raise DropItem('%s already has a record for %s' %
                           (item['facility'], item['date'].isoformat()))

        facility = self.get_or_create_facility(item['facility'])
        census = Census(facility=facility, date=item['date'])


        for field in item.ordered_fields:

            if field not in ['facility', 'date']:
                val = item.get(field, None)

                if val is not None:
                    setattr(census, field, val)

        self.session.add(census)
        self.session.commit()

        return item

    def get_or_create_facility(self, name):
        '''Return the Facility for the provided name.'''

        facility = self.session.query(Facility).filter_by(
                   name=name).one_or_none()

        if facility is None:
            fc = Facility(name=name)
            self.session.add(fc)
            self.session.commit()
            return fc

        return facility

    def census_exists(self, facility_name, date):
        '''Return Bool indicating whether a census exists for the given facility
        and date
        '''

        census = self.session.query(Census).join(Facility).\
                 filter(Census.date==date).filter(Facility.name==facility_name).one_or_none()

        if census is None:
            return False

        return True
