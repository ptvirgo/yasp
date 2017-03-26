# -*- coding: utf-8 -*-

import unittest
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import Session

import config
import jailjawn

class DatabaseTest(unittest.TestCase):
    '''Ensure the JailJawn database connects.'''

    def setUp(self):
        engine = create_engine(config.test_db_url)
        self.connection = engine.connect()
        jailjawn.Base.metadata.create_all(self.connection)

    def tearDown(self):
        jailjawn.Base.metadata.drop_all(self.connection)
        self.connection.close()

    def test_facility_name(self):
        '''Running this test mostly just proves that the database connection
           succeeded and the library loaded.
        '''
        d13 = jailjawn.Facility(name='D13')
        self.assertEqual(d13.name, 'D13')
        
if __name__ == '__main__':
    unittest.main()
