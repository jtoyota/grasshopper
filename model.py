#!/usr/bin/python
#marinabichoffe hackbright final project
import correlation
from math import ceil
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################
# Model definitions


class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=True)
    is_mentor = db.Column(db.Boolean, default=False)
    active_since = db.Column(db.TIMESTAMP)
    location = db.Column(db.String(80), nullable=True)
    country_code = db.Column(db.String(2),
                             db.ForeignKey('countries.country_code'))
    industry_code = db.Column(db.Integer,
                              db.ForeignKey('industries.industry_code'))
    num_connections = db.Column(db.Integer)
    num_connections_capped = db.Column(db.Boolean, default=False)
    summary = db.Column(db.String(2000))
    headline = db.Column(db.String(400))
    picture_url = db.Column(db.String(400))
    fun_facts = db.Column(db.String(1000), nullable=True)

    # Define relationship to country
    country = db.relationship("Country",
                              backref=db.backref("users",
                                                 order_by=user_id))

    # Define relationship to industry
    industry = db.relationship("Industry",
                               backref=db.backref("users",
                                                  order_by=user_id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return """<User user_id={} email={}
            is_mentor={}>""".format(self.user_id, self.email, self.is_mentor)


    def serialize(self):

        return {'user_id': self.user_id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'active_since': self.active_since,
                'is_mentor': self.is_mentor,
                'location': self.location,
                'country': self.country.country_name,
                'summary': self.summary,
                'picture_url': self.picture_url,
                'industry': self.industry.description,
                'fun_facts': self.fun_facts,
                'positions': {'total': len(self.positions),
                              'values': [{
                                         'title': position.title,
                                         'summary': position.summary,
                                         'start_date': position.start_date,
                                         'is_current': position.is_current,
                                         'end_date': position.end_date,
                                         'company': position.company.name,
                                         } for position in self.positions]
                              },
                'hobbies': [u.hobby.description for u in self.userhobbies],
                'pets': [u.pet.species for u in self.userpets],
                'areas_score': [{'title': score.area.title, 'score': score.score} for score in
                                self.scores]
                }


    def similarity(self, other):
        """Return Pearson rating for user compared to other user."""
        u_scores = {}
        paired_scores = []

        # loop through user scores and add to dict, using area_id as key
        for s in self.scores:
            u_scores[s.area_id] = s

        # loop through other user ratings, check if area_id matches
        for s in other.scores:
            u_s = u_scores.get(s.area_id)
            if u_s:
                # put pair of ratings in paired scores list
                paired_scores.append( (u_s.score, s.score) )
        # feed pair list to pearson function
        if paired_scores:
            return correlation.pearson(paired_scores)
        else:
            return 0.0

    def find_matches(self):
        """Return list of users in decrescent order of pearson correlation."""
        if self.is_mentor:
            other_users = [ u for u in User.query.filter_by(is_mentor='False') ]
        else:
            other_users = [ u for u in User.query.filter_by(is_mentor='True') ]

        similarities = [
            (self.similarity(other_user), other_user)
            for other_user in other_users]

        similarities.sort(reverse=True)

        return similarities

class AreasOfInterest(db.Model):
    """Five "MY" areas of interest for mentors/mentees."""

    __tablename__ = "areas"

    area_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(100))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return """<Area of interest area_id={} title={}
            desciption={}>""".format(self.area_id, self.title,
                                     self.description)


class AreasOfInterestScore(db.Model):
    """Likert scale for areas of interest."""

    __tablename__ = "score"

    score_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.area_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("scores",
                                              order_by=score_id))

    # Define relationship to area
    area = db.relationship("AreasOfInterest",
                           backref=db.backref("scores",
                                              order_by=score_id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return """<Score score_id={} area_id={} user_id={}
            score={} >""".format(self.score_id, self.area_id, self.user_id,
                                 self.score)


class Country(db.Model):
    """The lower-case ISO 3166-1 standard country code and respective names."""

    __tablename__ = "countries"

    country_code = db.Column(db.String(2), primary_key=True)
    country_name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return """<Country code={}
        country_name={}>""".format(self.country_code, self.country_name)


class Company(db.Model):
    """Details about a company."""

    __tablename__ = "companies"

    company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    company_type = db.Column(db.String(60))
    industry_code = db.Column(db.Integer,
                              db.ForeignKey('industries.industry_code'))

    # Define relationship to industry
    industry = db.relationship("Industry",
                               backref=db.backref("companies",
                                                  order_by=company_id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return """< company_id={} name={}
        industry={}>""".format(self.company_id, self.name,
                               self.industry.description)


class Events(db.Model):
    """Types of events."""

    __tablename__ = "events"

    event_code = db.Column(db.String(4), primary_key=True)
    event_type = db.Column(db.String(50))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<Events event_code={} event_type={}".format(self.event_code,
                                                            self.event_type)


class Hobbies(db.Model):
    """List of hobbies available for user to choose from."""

    __tablename__ = 'hobbies'

    hobby_code = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group = db.Column(db.String(60))
    description = db.Column(db.String(100))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return """<Hobbies hobby_code={}  group={}
                description={}>""".format(self.hobby_code, self.group,
                                          self.description)


class Industry(db.Model):
    """Details about a specific industry."""

    __tablename__ = "industries"

    industry_code = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(20))
    description = db.Column(db.String(100))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return """<Industry industry_code={} group={}
        description={}>""".format(self.industry_code,
                                  self.group, self.description)


class Mentorship(db.Model):
    """Connection between mentor and mentee."""

    __tablename__ = "mentorships"

    mentorship_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    mentorship_code = db.Column(db.String(4),
                                db.ForeignKey(
                                    'mentorship_types.mentorship_code'))
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    mentee_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    is_active = db.Column(db.Boolean)
    requester = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    accepted_request = db.Column(db.Boolean, default=False)
    mentorship_start_date = db.Column(db.TIMESTAMP)

    # Define relationship to mentor
    mentor = db.relationship("User",
                             foreign_keys=[mentor_id],
                             backref=db.backref("mentorships",
                                                order_by=mentorship_id))

    # Define relationship to mentee
    mentee = db.relationship("User",
                             foreign_keys=[mentee_id],
                             backref=db.backref("menteeships",
                                                order_by=mentorship_id))

    # Define relationship to mentorship type
    mentorship_type = db.relationship("MentorshipType",
                                      backref=db.backref("mentorships",
                                                         order_by=mentorship_id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return """<Mentorship mentorship_id={} mentorship_code={} mentor_id={}
            mentee_id={} is active={}>""".format(self.mentorship_id,
                                                 self.mentorship_code,
                                                 self.mentor_id,
                                                 self.mentee_id,
                                                 self.is_active)


class MentorshipType(db.Model):
    """Types of connectios between mentors and mentees."""

    __tablename__ = "mentorship_types"

    mentorship_code = db.Column(db.String(3), primary_key=True)
    connection_type = db.Column(db.String(40))
    mentorship_description = db.Column(db.String(500))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return """<Mentorship Type mentorship_code={} connection_type={}
            mentorship_description={}>""".format(self.mentorship_code,
                                                 self.connection_type,
                                                 self.mentorship_description)


class Pets(db.Model):
    """Details about pets owned by user."""

    __tablename__ = "pets"

    pet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    species = db.Column(db.String(40))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<Pets pet_id={} species={}".format(self.pet_id,
                                                   self.species)


class Position(db.Model):
    """Details about user's current position."""

    __tablename__ = "positions"

    position_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    title = db.Column(db.String(80), nullable=False)
    summary = db.Column(db.String(700))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime, nullable=True)
    is_current = db.Column(db.Boolean)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'))

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("positions",
                                              order_by=position_id))
    # Define relationship to company
    company = db.relationship("Company",
                              backref=db.backref("positions",
                                                 order_by=position_id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return """<Position position_id={}  user_id={} title={}
        company_id={} company_name= {}>""".format(self.position_id,
                                                  self.user_id,
                                                  self.title,
                                                  self.company_id,
                                                  self.company.name)
class ScheduledEvents(db.Model):
    """Events related to mentorship relationship."""

    __tablename__ = "scheduled_events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_code = db.Column(db.String(4), db.ForeignKey('events.event_code'))
    mentorship_id = db.Column(db.Integer,
                              db.ForeignKey('mentorships.mentorship_id'))
    title = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime)
    attachments = db.Column(db.LargeBinary, nullable=True)

    # Define relationship to mentorship
    mentorship = db.relationship("Mentorship",
                                 backref=db.backref("scheduled_events",
                                                    order_by=event_id))
    event_type = db.relationship("Events",
                                 backref=db.backref("scheduled_events",
                                                    order_by=event_id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return """<Events event_id={} event_code={}
                mentorship_id={} title={} date={}""".format(self.event_id,
                                                            self.event_code,
                                                            self.title,
                                                            self.date)


class UserHobbies(db.Model):
    """Association table between Hobbies and User."""

    __tablename__ = "userhobbies"

    userhobbies_id = db.Column(db.Integer, autoincrement=True,
                               primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    hobby_code = db.Column(db.Integer, db.ForeignKey('hobbies.hobby_code'))

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("userhobbies",
                                              order_by=userhobbies_id))
    hobby = db.relationship("Hobbies",
                            backref=db.backref("userhobbies",
                                               order_by=userhobbies_id))
    def __repr__(self):
        """Provide helpful representation when printed."""
        return """<Userhobbies userhobbies_id={}  user_id={}
                  hobby_code={}>""".format(self.userhobbies_id, self.user_id,
                                           self.hobby_code)


class UserPets(db.Model):
    """Association table between Hobbies and User."""

    __tablename__ = "userpets"

    userpets_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.pet_id'))

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("userpets",
                                              order_by=userpets_id))
    pet = db.relationship("Pets",
                          backref=db.backref("userpets",
                                             order_by=userpets_id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return """<UserPets userpets_id={}  user_id={}
                  pet_id={}>""".format(self.userpets_id, self.user_id,
                                       self.pet_id)

class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""
    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///grasshopper'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
