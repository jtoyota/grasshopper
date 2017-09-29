#!/usr/bin/python -tt
#marinabichoffe hackbright final project

import datetime
from sqlalchemy import func
from model import User, Country, connect_to_db, db
import datapackage
import json
from server import app

##############################################################################
# Seed database

def load_countries():
    """Load list of ISO 3166-1 alpha-2 countries with 2 digit codes to db."""

    print "Countries"

    f = open("data_source/countries_json.json")
    dicts = f.read()
    #decode json file into python list of dictionaries
    dicts = json.loads(dicts)
    for d in dicts:
        country = Country(country_code=d['Code'],
                          country_name=d['Name'])

        db.session.add(country)
        # We need to add to the session or it won't ever be stored

    # Once we're done, we should commit our work
    db.session.commit()

def load_industries():
    """Load list of industry codes as referenced by linkedin."""

    f = open("data_source/industry_codes")

    for line in f:
        print line
        #unpack data 
        industry_code, group, description = line.split("\t")

        industry = Industry(industry_code=industry_code,
                            group=group,
                            description=description)

        # add to session
        db.session.add(industry)


    db.session.commit()


def load_pets():
    pass


def load_hobbies():
    pass

def load_mentorship_types():
    pass





if __name__ == "__main__":
    connect_to_db(app)
    db.drop_all()
    db.create_all()
    load_countries()
    load_industries()
