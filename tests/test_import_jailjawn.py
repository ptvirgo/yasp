# -*- coding: utf-8 -*-

from import_jailjawn import JailJawnImporter
import jailjawn
import unittest
import config
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys

class TestUpdateHelpers(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine(config.test_db_url)
        connection = self.engine.connect()
        jailjawn.Base.metadata.create_all(connection)
        connection.close()

        self.test_connection = self.engine.connect()
        Session = sessionmaker(bind=self.test_connection)
        self.session = Session()
        self.jj = JailJawnImporter(self.session)

    def tearDown(self):

        self.test_connection.close()
        self.session.close()
        jailjawn.Base.metadata.drop_all(self.engine)

    def test_facility(self):
        d13 = jailjawn.Facility(name='D13')
        self.assertEqual(d13.name, 'D13')
        

    def test_facility_name(self):
        self.assertEqual(self.jj.facility_name('DC-PHSW'), 'DC-PHSW')
        self.assertEqual(self.jj.facility_name('Delaware   County'),
            'Delaware County')
        self.assertEqual(self.jj.facility_name(
            'PDP   Headcount + NIF '), 'PDP Headcount + NIF')
        self.assertEqual(self.jj.facility_name(
            'PPS   "In Facility" (Count)'),
            'PPS "In Facility" (Count)')

    def test_dict2census(self):
        data = {
            'In Out Male' : 0,
            'In Out Female' : 0,
            'Emergecy Room Trip Female' : 0,
            'Facility Name' : '  DC-PHSW',
            'Total Count' : 53,
            'Open Ward Male' : 1,
            'Furlough Female' : 0,
            'Furlough Male' : 0,
            'Worker Female' : 0,
            'Adult Female' : 4,
            'Open Ward Female' : 0,
            'Juvenile Male' : 0,
            'Adult Male' : 48,
            'Juvenile Female' : 0,
            'Worker Male' : 0,
            'Emergecy Room Trip Male' : 0
        }
        phsw = self.jj.dict2census(date.today(), data)
        self.assertEqual(phsw.facility.name, 'DC-PHSW')
        self.assertEqual(phsw.total_count, 53)
        self.assertEqual(phsw.date, date.today())

        self.assertRaises(ValueError, self.jj.dict2census, date.today(), data)

    def test_census_taken(self):
        data = {
            'In Out Male' : 0,
            'In Out Female' : 0,
            'Emergecy Room Trip Female' : 0,
            'Facility Name' : '  DC-PHSW',
            'Total Count' : 53,
            'Open Ward Male' : 1,
            'Furlough Female' : 0,
            'Furlough Male' : 0,
            'Worker Female' : 0,
            'Adult Female' : 4,
            'Open Ward Female' : 0,
            'Juvenile Male' : 0,
            'Adult Male' : 48,
            'Juvenile Female' : 0,
            'Worker Male' : 0,
            'Emergecy Room Trip Male' : 0
        }

        self.assertFalse(self.jj.census_taken(date.today()))
        phsw = self.jj.dict2census(date.today(), data) 
        self.assertTrue(self.jj.census_taken(date.today()))
