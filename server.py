# marinabichoffe hackbright final project
import os
from pprint import pformat
import requests
from jinja2 import StrictUndefined
import json
from flask import Flask, render_template, request, flash, redirect, session, \
    jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import *
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "BURNAFTERREADING"


LINKEDIN_CLIENT_ID = os.environ.get('CLIENT_ID')

LINKEDIN_CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

LINKEDIN_URL = "https://api.linkedin.com"

RETURN_URL = 'http://localhost:5000/oauth'

STATE = '9493953985'

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
    """Redirect to mentor ergistration flow."""
    session['user_type'] = 'mentor'
    return render_template('mentor_register.html')


@app.route('/areas_of_interest', methods=['GET', 'POST'])
def show_areas_of_interest():
    """Store areas of interest in session."""
    return render_template('areas_of_interest.html')


@app.route('/areas_of_interest.json', methods=['POST'])
def get_areas_of_interest():
    """Store areas of interest in session."""

    # store in session to add to db later
    session['areas_of_interest'] = {
        'my_style': int(request.form.get('my_style')),
        'my_career': int(request.form.get('my_career')),
        'my_craft': int(request.form.get('my_life')),
        'my_world': int(request.form.get('my_world'))
    }

    # this dict will be used in autocomplete function in mentor_register.js
    pets_and_hobbies = {
        "hobbies": get_hobbies(),
        "pets": get_pets()
    }
    print pets_and_hobbies
    return jsonify(pets_and_hobbies)


@app.route('/hobbies_and_pets.json', methods=['POST'])
def get_hobbies_and_pets():
    """Store areas of interest in session."""
    session['user_hobbies'] = request.form.get('hobbies').strip('\n').split(",")
    session['user_pets'] = request.form.get('pets').strip('\n').split(",")

    return render_template("/create_account.html")


@app.route('/mentee_registration')
def mentee_registration():
    pass


@app.route('/create_account')
def create_account():
    """Render first time sign in page."""
    return render_template("create_account.html")


@app.route("/register")
def show_linkedin_registration():
    """Redirect user to LinkedIn's Approve/Deny page"""

    return redirect("https://www.linkedin.com/oauth/v2/authorization"
                    + "?response_type=code"
                    + "&client_id=" + LINKEDIN_CLIENT_ID
                    + "&redirect_uri=" + RETURN_URL
                    + "&state=" + STATE)


@app.route("/oauth")
def oauth_process():
    """Get user data using OAuth"""

    code = request.args.get('code')

    #for deployment only:
    #state = request.args.get('state')
    # A value used to test for possible CSRF attacks.
    #if state != STATE:
    #throw HTTP 401 error
    if code:
        access_token = get_access_token(code)


        if access_token:
            print "access token", access_token
            get_user_data(access_token)

    # If there is no access code, flash an error message
    else:
        error_code = request.args.get('error')
        error_description = request.args.get('error_description')
        print "error"
        flash('OAuth failed')

    return redirect('/create_account')


######### Helper Functions #########
def get_access_token(code):
    """Use access code to request user's access token"""

    payload = {'grant_type': 'authorization_code',
               'code': code,
               'redirect_uri': RETURN_URL,
               'client_id': LINKEDIN_CLIENT_ID,
               'client_secret': LINKEDIN_CLIENT_SECRET
               }

    response = requests.post("https://www.linkedin.com/uas/oauth2/accessToken",
                             data=payload)
    json = response.json()

    # If the response was successful, use the access token from the returned JSON
    if response.ok:
        access_token = json['access_token']

    # If there was an error, use None as the access token and
    # flash a message
    else:
        access_token = None
        flash('OAuth failed: ' + json['error_description'])

    return access_token


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


######### Helper Functions #########


def get_hobbies():
    """return a list of hobbies"""

    hobbies = db.session.query(Hobbies.description)
    hobbies_list = [h.description for h in hobbies]
    return hobbies_list

def get_pets():
    """return a list of hobbies"""

    pets = db.session.query(Pets.species)
    pets_list = [p.species.rstrip() for p in pets]
    return pets_list


def get_user_data(access_token):
    """Use user's access token to get profile data from linkedin."""

    headers = {'Authorization': 'Bearer' + access_token}
    user_data = '('\
    +'first-name,'\
    +'last-name,'\
    +'email-address,'\
    +'headline,'\
    +'summary,'\
    +'location,'\
    +'positions,'\
    +'picture-urls::(original))'

    response = requests.get(LINKEDIN_URL
                            + "/v1/people/~:"
                            + user_data
                            +"?format=json",
                            headers=headers)
    data = response.json()

# If the response was successful (with a status code of less than 400),
# use the list of events from the returned JSON
    if response.ok:
        print data

# If there was an error (status code between 400 and 600), use an empty list
    else:
        flash("Error: " + data['message'] + 'status' + data['status'])
        user_data = []
    # Create a dictionary of the events with ids as keys and names as values
    # events_dict = {}
    # for event in events:
    #     event_id = event['id']
    #     event_name = event['name']['text']
    #     events_dict[event_id] = event_name

    # return render_template("my-events.html",
    #                        events=events_dict,
    #                        data=pformat(data))
    # payload = {'event_id': event_id}
    # headers = {'Authorization': 'Bearer ' + access_token}

    # response = requests.post(EVENTBRITE_URL + "users/me/bookmarks/save/",
    #                          data=payload,
    #                          headers=headers)
    # json = response.json()

    # # If the response was successful and returned JSON has the value True
    # # for the 'created' key
    # if response.ok and json['created']:
    #     flash('Bookmark saved! https://www.eventbrite.com/e/' + event_id)
    # else:
    #     flash('Bookmark not saved: ' + json['error_description'])



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
