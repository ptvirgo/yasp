# YASP Counter

There are young people (juveniles, under the age of 18) locked up in adult
prison in Philadelphia.  This suite keeps a count of them for the [Youth Art and
Self-Empowerment Project (YASP)](http://www.yasproject.com/).

Certain aspects of the tool are over-engineered for a simple counter.  A
secondary goal of the project has been to practice using more advanced
libraries and techniques.

## Sources

There is historical data collected from the
[JailJawn](https://jailjawn.github.io/) [Code for Philly
project](https://codeforphilly.org/).  Ongoing updates are collected directly
from the [Philadelphia prison
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

## Configuration notes

Export CENSUS_DB to a SQLAlchemy database url, such as

```bash
   export CENSUS_DB=postgresql://readonly_user:password@example.com/real
```

or

```bash
   export CENSUS_DB=sqlite3:////$HOME/dir/census.db
```

Prepare the database tables with an interactive shell:

```python
census.db_tools.create()
```

Capture the latest census data:
```bash
scrapy crawl census_page
```
