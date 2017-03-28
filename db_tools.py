# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from core import Base, Census, Facility


def create(url):
    engine = create_engine(url)
    Base.metadata.create_all(engine)

def destroy(url):
    engine = create_engine(url)
    Census.__table__.drop(engine)
    Facility.__table__.drop(engine)
