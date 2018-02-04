# -*- coding: utf-8 -*-

import os

from sqlalchemy import create_engine
from census import Base, Census, Facility


def create(url=os.environ['CENSUS_DB']):
    engine = create_engine(url)
    Base.metadata.create_all(engine)


def destroy(url=os.environ['CENSUS_DB']):
    engine = create_engine(url)
    engine = create_engine(url)
    Census.__table__.drop(engine)
    Facility.__table__.drop(engine)
