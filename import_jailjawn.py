# -*- coding: utf-8 -*-

from dateutil.parser import parse
from jailjawn import Census, Facility
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import write_db_url
import re
import requests


class JailJawnImporter(object):

    def __init__(self, session):
        '''The importer requires a prepared SQL Alchemy session.
        '''
        self.session = session
        self.jailjawn_url = 'https://jailjawnapi.herokuapp.com/all'

    def facility_name(self, text):
        '''Clean facility names'''
        unspaced = re.sub('[\s]+', ' ', text.strip())
        return unspaced

    def dict2census(self, date, data):
        '''Convert single JailJawn JSON dictionary to a Census record'''

        f_name = self.facility_name(data['Facility Name'])

        facility = self.session.query(Facility).filter_by(name=f_name).first()

        if facility is None:
            facility = Facility(name=f_name)
            self.session.add(facility)
            self.session.flush()

        census = self.session.query(Census).filter_by(
            date=date, facility=facility).first()

        if census is not None:
            self.session.rollback()
            raise ValueError('Duplicate census entry ' + str(census))

        census = Census(
            facility=facility,
            date=date,
            adult_female=data.get('Adult Female'),
            adult_male=data.get('Adult Male'),
            emergency_room_trip_female=data.get('Emergency Room Trip Female'),
            emergency_room_trip_male=data.get('Emergency Room Trip Male'),
            furlough_female=data.get('Furlough Female'),
            furlough_male=data.get('Furlough Male'),
            in_out_female=data.get('In Out Female'),
            in_out_male=data.get('In Out Male'),
            juvenile_female=data.get('Juvenile Female'),
            juvenile_male=data.get('Juvenile Male'),
            open_ward_female=data.get('Open Ward Female'),
            open_ward_male=data.get('Open Ward Male'),
            total_count=data.get('Total Count'),
            worker_female=data.get('Worker Female'),
            worker_male=data.get('Worker Male')
        )
        self.session.add(census)
        self.session.commit()
        return census

    def census_taken(self, date):
        '''Given a date, return true if the census has already been recorded
           for that date, false otherwise.
        '''
        census = self.session.query(Census).filter_by(date=date).first()
        return census is not None

    def import_census(self):
        r = requests.get(self.jailjawn_url)

        if r.status_code != 200:
            raise requests.exceptions.ConnectionError(
              'Could not reach ' + self.jailjawn_url)

        count = 0
        jsr = r.json()

        for cd in jsr:
            census_date = parse(cd)

            if not self.census_taken(census_date):

                for fac in jsr[cd]:
                    census = self.dict2census(census_date, jsr[cd][fac])
                    if census is not None:
                        count += 1
        return count


if __name__ == "__main__":
    engine = create_engine(write_db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    jj = JailJawnImporter(session)
    records = jj.import_census()
