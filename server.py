#!/usr/bin/python
#marinabichoffe hackbright final project
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import * 

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "BURNAFTERREADING"

@app.route('/')
def index():
    """Splash page."""

    return render_template("/index.html")

@app.route('/about')
def about_page():

    render_template("/about")

@app.route('/mentor_registration/')
def mentor_registration():
    pass

@app.route('/mentee_registration/')
def mentee_registration():
    pass


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
