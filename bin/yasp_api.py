# -*- coding: utf-8 -*-

from dateutil.parser import parse
from flask import Flask, jsonify
from jailjawn import Census, Facility
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config

app = Flask(__name__)

def format_census(c):
    date = str('%d-%d-%d' % (c.date.year, c.date.month, c.date.day))
    return {
        'date': date,
        'juvenile_male': c.juvenile_male,
        'juvenile_female': c.juvenile_female,
        'total': c.juvenile_male + c.juvenile_female}

@app.route('/api/census', methods=['GET'])
def census():

    engine = create_engine(config.db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    census_data = session.query(Census)\
        .join(Facility)\
        .filter(Facility.name=='PDP "In Facility" Count')\
        .order_by(Census.date.desc())

    counts = []

    for c in census_data:
        counts.append(format_census(c))

    return jsonify(counts)

@app.route('/api/census/latest', methods=['GET'])
def latest():
    engine = create_engine(config.db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    c = session.query(Census)\
        .join(Facility)\
        .filter(Facility.name=='PDP "In Facility" Count')\
        .order_by(Census.date.desc())\
        .limit(1)\
        .one()

    return jsonify(format_census(c))

@app.route('/api/census/<string:day>')
def census_from(day):
    engine = create_engine(config.db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    error = {'error': 'invalid date'}

    try:
        date = parse(day)
    except:
        return (jsonify(error), 400)

    try:
        c = session.query(Census)\
            .join(Facility)\
            .filter(Census.date==date)\
            .filter(Facility.name=='PDP "In Facility" Count')\
            .one()
        return jsonify(format_census(c))
    except:
        return (jsonify(error), 400)

if __name__ == '__main__':
    app.run()
