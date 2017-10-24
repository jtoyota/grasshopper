# marinabichoffe hackbright final project
import os
from pprint import pformat
from datetime import datetime
import dateutil
import pytz
from tzlocal import get_localzone
import requests
from jinja2 import StrictUndefined
import json
from flask import Flask, render_template, request, flash, redirect, session, \
    jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import *
# import calendar
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "BURNAFTERREADING"


LINKEDIN_CLIENT_ID = os.environ.get('CLIENT_ID')

LINKEDIN_CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

LINKEDIN_URL = "https://api.linkedin.com"

RETURN_URL = 'http://localhost:5000/oauth'

STATE = '9493953985'

TZ = get_localzone()

PER_PAGE = 10

@app.route('/')
def index():
    """Main page."""

    return render_template("index.html")


@app.route('/about')
def about():
    """Info about the program."""
    return render_template("/about.html")


@app.route('/add_to_calendar')
def add_to_calendar():
    """add event to google calendar API"""
    event_id = None
    start = None
    end = None
    summary = None
    email = None
    # calendar.add_event()
    pass


@app.route('/connection_requests/<status>.json')
def show_pending_requests(status='pending_requests'):
    """return json file of all pending requests."""
    print status
    requester = session['user_id']
    requests = []
    if status == 'pending_requests':
        if session['mentor']:
            requests_query = Mentorship.query.options(
                db.joinedload('mentee')).filter_by(mentor_id=requester,
                                                   accepted_request='False').all()
        elif session['mentee']:
            requests_query = Mentorship.query.options(
                db.joinedload('mentee')).filter_by(mentee_id=requester,
                                                   accepted_request='False').all()
    elif status == 'sent_requests':
        if session['mentor']:
                requests_query = Mentorship.query.options(
                    db.joinedload('mentee')).filter_by(mentor_id=requester,
                                                       accepted_request='False').all()
        elif session['mentee']:
            requests_query = Mentorship.query.options(
                db.joinedload('mentee')).filter_by(mentee_id=requester,
                                                   accepted_request='False').all()
    else:
        return flash('invalid request')
        print session['mentor'], session['is_mentor']

    for r in requests_query:
        req_info = {}
        req_info['mentorship_id'] = r.mentorship_id
        req_info['mentee_info'] = r.mentee.serialize()
        requests.append(req_info)

    return jsonify(requests)


@app.route('/accept_request/')
def accept():
    """Activate mentorship on db."""
    mentorship_id = request.args.get('mentorship_id')
    mentorship = Mentorship.query.get(mentorship_id)
    if mentorship:
        mentorship.is_active=True
        mentorship.accept_request=True
        mentorship.start_date=datetime.utcnow().isoformat() + 'Z'# 'Z' indicates UTC time
        db.session.commit()
        return 'Request accepted'
    return none

@app.route('/all_matches.json')
def show_matches():
    """Returns a list of matches."""

    users = get_matches()

    return jsonify(users)

@app.route('/areas_of_interest', methods=['GET', 'POST'])
def show_areas_of_interest():
    """Store areas of interest in session."""
    return render_template('areas_of_interest.html')


@app.route('/areas_of_interest.json', methods=['POST'])
def get_areas_of_interest():
    """Store areas of interest in session."""
    # store in session to add to db later
    session['areas_of_interest'] = {
        'My Style': int(request.form.get('my_style')),
        'My Career': int(request.form.get('my_career')),
        'My Craft': int(request.form.get('my_craft')),
        'My life': int(request.form.get('my_life')),
        'My World': int(request.form.get('my_world'))
    }

    # this dict will be used in autocomplete function in mentor_register.js
    pets_and_hobbies = {
        "hobbies": get_hobbies(),
        "pets": get_pets()
    }
    return jsonify(pets_and_hobbies)


@app.route('/login')
def login():
    """Render first time sign in page."""
    return render_template("login.html")


@app.route('/hobbies_and_pets.json', methods=['POST'])
def get_hobbies_and_pets():
    """Store areas of interest in session."""
    session['user_hobbies'] = request.form.get('hobbies').strip('\n').split("|")
    session['user_pets'] = request.form.get('pets').strip('\n').split("|")

    if not session['user_hobbies'] and not session['user_pets']:
        return 'error, try again'
    return 'ok'


@app.route('/home')
def main_page():
    """Render user's main page."""
    user_id = User.query.filter_by(email='bichoffe.marina@gmail.com').one().user_id
    session['user_id'] = user_id
    user = User.query.get(user_id).serialize()

    return render_template("home.html", user=user)

@app.route('/request_connection', methods=['POST'])
def make_request():
    """create a mentorship on db with pending status."""

    requester = session['user_id']
    mentorship_code = 'one' # setting one-on-one as default for now
    if session['mentor']:
        mentor_id = session['user_id']
        mentee_id = int(request.form.get('user_id'))
    elif session['mentee']:
        mentee_id = session['user_id']
        mentor_id = request.form.get('user_id')

    new_mentorship = Mentorship(mentorship_code=mentorship_code,
                                mentor_id=mentor_id,
                                mentee_id=mentee_id,
                                requester=requester)
    db.session.add(new_mentorship)
    db.session.commit()
    print new_mentorship


@app.route('/mentor_registration')
def mentor_registration():
    """Redirect to mentor ergistration flow."""
    session['user_type'] = 'mentor'
    session['mentor'] = True

    return render_template('mentor_register.html')



@app.route('/notifications')
def show_notifications():
    """render notifications page."""
    user_id = session['user_id']
    user = User.query.get(user_id).serialize()
    return render_template("notifications.html", user=user)


@app.route('/oauth')
def oauth_process():
    """Get user data using OAuth"""

    code = request.args.get('code')

    # for deployment only:
    # state = request.args.get('state')
    # A value used to test for possible CSRF attacks.
    # if state != STATE:
    # throw HTTP 401 error
    if code:
        access_token = get_access_token(code)
        if access_token:
            get_user_data(access_token)
            return redirect("/profile")

        error_code = request.args.get('error')
        error_description = request.args.get('error_description')

        flash('OAuth failed error: {} {}'.format(error_code, error_description))
        return redirect('/create_account')

    # If there is no access code, flash an error message
    else:
        error_code = request.args.get('error')
        error_description = request.args.get('error_description')

        flash('OAuth failed error: {} {}'.format(error_code, error_description))
        return redirect('/create_account')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/profile')
@app.route('/profile/<current>')
def profile(current='bm'):
    """Render user profile's main page."""
    user_id = User.query.filter_by(email='bichoffe.marina@gmail.com').one().user_id
    session['user_id'] = user_id
    user = User.query.get(user_id).serialize()

    return render_template("profile.html", user=user, current=current)


@app.route('/register')
def show_linkedin_registration():
    """Redirect user to LinkedIn's Approve/Deny page."""
    return redirect("https://www.linkedin.com/oauth/v2/authorization"
                    + "?response_type=code"
                    + "&client_id=" + LINKEDIN_CLIENT_ID
                    + "&redirect_uri=" + RETURN_URL
                    + "&state=" + STATE)

@app.route('/search')
def search_for_users():
    pass




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
                + 'first-name,'\
                + 'last-name,'\
                + 'email-address,'\
                + 'industry,'\
                + 'headline,'\
                + 'summary,'\
                + 'location,'\
                + 'positions,'\
                + 'num-connections,'\
                + 'num-connections-capped,'\
                + 'picture-urls::(original))'

    response = requests.get(LINKEDIN_URL
                            + "/v1/people/~:"
                            + user_data
                            + "?format=json",
                            headers=headers)
    data = response.json()

# If the response was successful (with a status code of less than 400),
# use the data dict from the returned JSON to create a new user
    if response.ok:
        load_user_data(data)
# If there was an error (status code between 400 and 600), use an empty list
    else:
        flash("Error: " + data['message'] + 'status', data['status'])
        print 'error'
        user_data = []


def load_user_data(data):
    """Add user data to database."""

    #User info
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['emailAddress']
    is_mentor = session['mentor']
    active_since = datetime.now(TZ)
    location = data['location']['name']
    country_code = (data['location']['country']['code']).upper()
    #query database for the correspondent industry code 
    industry_code = Industry.query.filter_by(
        description=data['industry']).first().industry_code
    num_connections = data['numConnections']
    num_connections_capped = data['numConnectionsCapped']
    headline = data['headline']
    summary = data['summary']
    picture_url = data['pictureUrls']['values'][0]
    #positions is a separate table with user_id as foreign key
    positions = data.get('positions')

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        is_mentor=is_mentor,
        summary=summary,
        active_since=active_since,
        location=location,
        country_code=country_code,
        industry_code=industry_code,
        num_connections=num_connections,
        num_connections_capped=num_connections_capped,
        headline=headline,
        picture_url=picture_url)

    db.session.add(new_user)
    db.session.commit()
    # Once user is created we can instantiate other classes that require
    # user_id as foreign key
    get_user_id(email)
    # Pass in the information collected from dictionary
    add_position(positions)
    #add user's pets and hobbies to db now that we have an user_id
    add_pets_hobbies()
    #add user's areas scores to db
    add_user_scores()
    print 'user added'


def get_user_id(user_email):
    """Get user id from db and save in session."""
    # get user id from database
    user_id = User.query.filter_by(email=user_email).one().user_id
    session['user_id'] = user_id


def add_position(positions):
    """Add user position to db."""
    user_id = session['user_id']
    for position in positions['values']:
        # search db for company, will return company id
        company_id = add_or_get_company(position['company'])
        title = position.get('title')
        summary = position.get('summary')
        is_current = position.get('isCurrent')
        s_month = str(position.get('startDate').get('month'))
        s_year = str(position.get('startDate').get('year'))
        start_date = datetime.strptime((s_month + s_year), "%m""%Y")
        end_date = None
        # if position isn't current, get end date
        if position.get('endDate'):
            e_month = str(position.get('endDate').get('month'))
            e_year = str(position.get('endDate').get('year'))
            end_date = datetime.strptime((s_month + s_year), "%m""%Y")

        new_position = Position(
            user_id=user_id,
            title=title,
            summary=summary,
            is_current=is_current,
            start_date=start_date,
            end_date=end_date,
            company_id=company_id)
        db.session.add(new_position)
        db.session.commit()


def add_or_get_company(company):
    """Search db for existing company or add new company."""
    comp = Company.query.filter_by(name=company['name']).first()
    if comp:
        return comp.company_id
    name = company['name']
    company_type = company['type']
    # query db for correspondent industry code
    industry_code = Industry.query.filter_by(
        description=company['industry']).first().industry_code
    # add new company to db
    new_company = Company(
        name=name,
        company_type=company_type,
        industry_code=industry_code)
    db.session.add(new_company)
    db.session.commit()

    company = Company.query.filter_by(name=company['name']).first()

    return company.company_id


def add_pets_hobbies():
    """Add user pets and hobbies to db. """
    user_id = session['user_id']
    for pet in session['user_pets']:
        pet_id = Pets.query.filter_by(species=pet).first().pet_id
        new_pet = UserPets(
            user_id=user_id,
            pet_id=pet_id)
        db.session.add(new_pet)
        db.session.commit()
    #iterate over list of hobbies saved in session and add to db    
    for hobby in session['user_hobbies']:
        hobby_code = Hobbies.query.filter_by(
            description=hobby).first().hobby_code
        new_hobby = UserHobbies(
            user_id=user_id,
            hobby_code=hobby_code)
        db.session.add(new_hobby)
        db.session.commit()


def add_user_scores():
    """Add user scores to db."""
    user_id = session['user_id']
    for area, score in session['areas_of_interest'].iteritems():
        area_id = AreasOfInterest.query.filter_by(
            title=area).first().area_id
        new_score = AreasOfInterestScore(
            area_id=area_id,
            user_id=user_id,
            score=score)
        db.session.add(new_score)
        db.session.commit()


def get_matches():
    """return list of matches."""
    user = User.query.get(session['user_id'])
    matches = user.find_matches()
    user_comp = []
    for match in matches:
        user_comp.append(match[1].serialize())

    return user_comp


# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(debug=True, host="0.0.0.0")
