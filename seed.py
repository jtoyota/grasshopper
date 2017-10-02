#!/usr/bin/python -tt
#marinabichoffe hackbright final project

import datetime
import re
from sqlalchemy import func
import datapackage
import json
from datetime import datetime
from server import app
from model import User, Country, Industry, Pets, Hobbies, AreasOfInterest, \
    Company, MentorshipType, connect_to_db, db

##############################################################################
# Seed database

def load_areas_of_interest():
    """Load areas of interest for mentorship."""

    f = open("data_source/areas_of_interest")
    for i, items in enumerate((f), 1):
        print items
        #unpack data
        title, description = items.split("\t")

        area = AreasOfInterest(area_id=i,
                               title=title,
                               description=description)

        # add to session
        db.session.add(area)
    db.session.commit()


def load_user():
    """Load mock dataset with user info."""

    f = open("data_source/user_data.txt")
    # list of users, divided by line:
    users = f.readlines()
    # unpack info
    for user_info in users[1:]:

        user_id, first_name, last_name, email, password, is_mentor, \
            active_since, country_code, industry_code, num_connections, \
            summary, picture_url, fun_facts = user_info.split("\t")

        user = User(user_id=user_id,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    is_mentor=is_mentor,
                    active_since=active_since,
                    country_code=country_code,
                    industry_code=industry_code,
                    num_connections=num_connections,
                    summary=summary,
                    picture_url=picture_url,
                    fun_facts=fun_facts)
        db.session.add(user)
    db.session.commit()


def load_companies():
    """Load list of mock companies."""

    f = open("data_source/mock_companies.txt")

    companies = f.readlines()
    # unpack info
    for comp in companies[1:]:
        company_id, name, company_type, industry_code = comp.split("\t")

        company = Company(company_id=company_id,
                          name=name,
                          company_type=company_type,
                          industry_code=industry_code.rstrip("\n"))
        db.session.add(company)
        db.session.commit()


def load_countries():
    """Load list of ISO 3166-1 alpha-2 countries with 2 digit codes to db."""

    f = open("data_source/countries_json.json")
    dicts = f.read()
    # decode json file into python list of dictionaries
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
        #unpack data
        industry_code, group, description = line.split("\t")
        #industry code included
        industry = Industry(industry_code=industry_code,
                            group=group,
                            description=description.rstrip('\n'))

        # add to session
        db.session.add(industry)
    db.session.commit()


def load_pets():
    """Load list of domestic animals."""

    f = open("data_source/pets_list")

    #read file and remove "s" from the end of characters, making it singular
    for i, line in enumerate((f), 1): # start at id 1
        line = re.sub(r'(\w*)(s)\b', r'\1', line).lower()
        pet = Pets(pet_id=i,
                   species=line)
         # add to session
        db.session.add(pet)

    db.session.commit()


def load_hobbies():
    """Load list of hobbies grouped by category"""

    f = open("data_source/hobbies", "r")
    # split text by hobby category
    text = f.read().split("||")
    # we will add hobbies as values and groups as keys in this dictionary
    hobbies_dict = {}

    for hobbies in text:
        # remove white spaces
        l = hobbies.split('\n')
        # set hobby category as key and create empty list
        hobbies_dict.setdefault(l[0], [])
        for hobbies in l[1:]:
            # remove unnecessary characters
            hobbies = re.sub(r'(\[\w*\])', r'', hobbies)
            # add to list
            if hobbies:
                hobbies_dict[l[0]].append(hobbies)

    # Each item in the list of hobbies will be added as a new hobby
    # With the dict key as group
    for key, value in hobbies_dict.iteritems():
        for v in value:
            hobby = Hobbies(group=key,
                            description=v)
            db.session.add(hobby)

    db.session.commit()


def load_mentorship_types():
    """Load list of mentorship types."""

    f = open("data_source/mentorship_types")

    for line in f:
        line.strip("\n")
        mentorship_code, connection_type, mentorship_description = line.split("\t")

        mentorship_type = MentorshipType(mentorship_code=mentorship_code,
                                         connection_type=connection_type,
                            mentorship_description=mentorship_description)

        db.session.add(mentorship_type)
        db.session.commit()

def load_events():
    pass


if __name__ == "__main__":
    connect_to_db(app)
    db.drop_all()
    db.create_all()

    load_countries()
    load_industries()
    load_pets()
    load_hobbies()
    load_areas_of_interest()
    load_user()
    load_companies()
    load_mentorship_types()
