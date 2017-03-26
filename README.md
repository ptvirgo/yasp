# YASP Counter

There are young people (juveniles, under the age of 18) locked up in adult
prison in Philadelphia.  This suite keeps a count of them for the [Youth Art and
Self-Empowerment Project (YASP)](http://www.yasproject.com/).

Certain aspects of the tool are over-engineered for a simple counter.  A
secondary goal of the project has been to experience using more advanced
libraries and techniques.

## Sources

We collect data directly from the [JailJawn](https://jailjawn.github.io/) Code
for Philly project, which in turn scrapes from the [Philadelphia prison
system's](http://www.phila.gov/prisons/Pages/default.aspx) daily census.

## API

The counter provides a simple JSON API for retrieving data.  Individual counts
take the form:

    {
        "date": "yyyy-mm-dd",
        "juvenile_female": integer,
        "juvenile_male": integer,
        "total": integer
    }
    
API endpoints are as follows:

- *api/census*: returns an array of all the available counts
- *api/census/latest*: returns the most recently available count
- *api/census/[date]*: [date] must be a valid date for which a census has been
  taken.  Returns the count for the provided date, or an error.


## Missing config

In the event that you'd like to run this thing yourself, it is necessary to add
a file *config.py* to the *bin* directory.  *config.py* must set a db_url
variable to a SQLAlchemy database url, and should set a test_db_url to another
one set aside for unittests.  Example:

    test_db_url="mysql://tester:test_password@example.com/unittest"
    db_url="postgresql://production:prod_password@example.com/real"

Yes, relying on file-system security is sub-optimal.  I'm happy to learn better
methods. For now the excuse is that this thing only hosts data that is already
public. 
