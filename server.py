#!/usr/bin/python
# marinabichoffe hackbright final project

from jinja2 import StrictUndefined
import json
from flask import Flask, render_template, request, flash, redirect, session, \
    jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import *

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "BURNAFTERREADING"


@app.route('/')
def index():
    """Splash page."""

    return render_template("index.html")


@app.route('/about')
def about():
    """Info about the program."""

    return render_template("/about.html")

@app.route('/mentor_registration')
def mentor_registration():
    session['user_type'] = 'mentor'
    return render_template('mentor_register.html')


@app.route('/areas_of_interest', methods=['GET', 'POST'])
def show_areas_of_interest():
    """Store areas of interest in session"""

    return render_template('areas_of_interest.html')

@app.route('/areas_of_interest.json', methods=['POST'])
def get_areas_of_interest():
    """Store areas of interest in session"""

    #store in session to add to db later
    session['areas_of_interest'] = {
        'my_style': int(request.form.get('my_style')),
        'my_career': int(request.form.get('my_career')),
        'my_craft': int(request.form.get('my_life')),
        'my_world': int(request.form.get('my_world'))
    }

    return jsonify(get_hobbies())

@app.route('/mentee_registration')
def mentee_registration():
    pass


def get_hobbies():
    """return a list of hobbies"""

    hobbies = db.session.query(Hobbies.description)
    hobbies_list = [h.description for h in hobbies]
    return hobbies_list



# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(debug=True, host="0.0.0.0")
