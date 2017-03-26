from sqlalchemy import Column, Date, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Census(Base):
    __tablename__ = 'census'
    id = Column(Integer, primary_key=True)
    date = Column(Date, index=True)
    facility_id = Column(SmallInteger, ForeignKey('facility.id'))
    facility = relationship('Facility', back_populates='reports')   
    adult_female = Column(SmallInteger)
    adult_male = Column(SmallInteger)
    emergency_room_trip_female = Column(SmallInteger)
    emergency_room_trip_male = Column(SmallInteger)
    furlough_female = Column(SmallInteger)
    furlough_male = Column(SmallInteger)
    in_out_female = Column(SmallInteger)
    in_out_male = Column(SmallInteger)
    juvenile_female = Column(SmallInteger)
    juvenile_male = Column(SmallInteger)
    open_ward_female = Column(SmallInteger)
    open_ward_male = Column(SmallInteger)
    total_count = Column(SmallInteger)
    worker_female = Column(SmallInteger)
    worker_male = Column(SmallInteger)

    def __repr__(self):
        return '<Census:(date=' + str(self.date) + ', facility=' \
             + str(self.facility) + ')>'
        

class Facility(Base):
    __tablename__ = 'facility'
    id = Column(SmallInteger, primary_key=True)
    name = Column(String(128), index=True, unique=True)
    reports = relationship('Census', back_populates='facility')

    def __repr__(self):
        return '<Facility:(name=' + str(self.name) + ')>'
