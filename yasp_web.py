# -*- coding: utf-8 -*-

from dateutil.parser import parse
from flask import Flask, jsonify, render_template
from jailjawn import Census, Facility
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import read_db_url

app = Flask(__name__)

def format_census(c):
    date = c.date.isoformat()
    return {
        'date': date,
        'juvenile_male': c.juvenile_male,
        'juvenile_female': c.juvenile_female,
        'total': c.juvenile_male + c.juvenile_female}

def connect():
    engine = create_engine(read_db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

@app.route('/', methods=['GET'])
def home():

    session = connect()

    c = session.query(Census)\
        .join(Facility)\
        .filter(Facility.name=='PDP "In Facility" Count')\
        .order_by(Census.date.desc())\
        .limit(1)\
        .one()

    d = format_census(c)

    body = str(
        '''<p>As of <span id="date">%s</span>, there are <span
id="total">%s</span> youth in Philadelphia adult jails.</p>
<div id="comic"></div>
<p><a href="http://www.yasproject.com/">YASP</a> is working to change that.</p>
        ''' % (d['date'], d['total']))

    scripts = [
        'https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/snap.svg/0.4.1/snap.svg-min.js',
        '/static/js/yasp_animation.js'
    ]

    return render_template('default.html',
        title="What's wrong with this picture?",
        body=body,
        scripts=scripts)

@app.route('/history', methods=['GET'])
def history():

    session = connect()

    census_data = session.query(Census)\
        .join(Facility)\
        .filter(Facility.name=='PDP "In Facility" Count')\
        .order_by(Census.date.desc())

    counts = []
    for c in census_data:
        counts.append(format_census(c))

    body='''<p>Thanks to <a href="https://jailjawn.github.io/">JailJawn</a> for
collecting the original census data.</p>'''

    return render_template('history.html',
        title='Historical Census',
        census=counts,
        body=body)

@app.route('/api/census', methods=['GET'])
def census():

    session = connect()

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
    session = connect()

    c = session.query(Census)\
        .join(Facility)\
        .filter(Facility.name=='PDP "In Facility" Count')\
        .order_by(Census.date.desc())\
        .limit(1)\
        .one()

    return jsonify(format_census(c))

@app.route('/api/census/<string:day>')
def census_from(day):
    session = connect()

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
