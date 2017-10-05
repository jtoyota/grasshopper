#!/usr/bin/python
# marinabichoffe hackbright final project

from jinja2 import StrictUndefined
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

    return render_template("/index.html")


@app.route('/about/')
def about():
    """Info about the program."""

    return render_template("/about")

@app.route('/mentor_registration/')
def mentor_registration():
    session['user_type'] = 'mentor'
    return render_template('mentor_register.html')

@app.route('/areas_of_interest/', methods=['POST', 'GET'])
def get_areas_of_interest():
    if request.method == 'POST':

        inputs = request.form.get('my_style')
        return "this"

    return render_template('/areas_of_interest.html')

@app.route('/mentee_registration/')
def mentee_registration():
    pass

    # melon = request.form.get('melon_type')
    # qty = int(request.form.get('qty'))

    # if qty > 10:
    #     result_code = 'ERROR'
    #     result_text = "You can't buy more than 10 melons"
    # elif qty > 0:
    #     result_code = 'OK'
    #     result_text = "You have bought %s %s melons" % (qty, melon)
    # else:
    #     result_code = 'ERROR'
    #     result_text = "You want to buy fewer than 1 melons? Huh?"




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
