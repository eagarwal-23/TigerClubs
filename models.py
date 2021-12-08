from datetime import time
from typing import DefaultDict
from app import db
from sqlalchemy.ext.hybrid import hybrid_property

DELETE_USER = 0
BLACKLIST_USER = 1
EDIT_USER = 2
EDIT_CLUB = 3
ADD_TAG = 4

# association tables
student_clubs = db.Table('student_clubs', 
                          db.Column('netid', db.String(), db.ForeignKey('student_info.netid')),
                          db.Column('clubid', db.Integer(), db.ForeignKey('club_info.clubid')))

student_tags = db.Table('student_tags', 
                        db.Column('netid', db.String(), db.ForeignKey('student_info.netid')),
                        db.Column('tagid', db.Integer(), db.ForeignKey('tag_info.tagid')))

student_reviews = db.Table('student_reviews', 
                        db.Column('reviewid', db.Integer(), db.ForeignKey('review_info.reviewid')),
                        db.Column('netid', db.String(), db.ForeignKey('student_info.netid')))

club_tags = db.Table('club_tags', 
                        db.Column('clubid', db.Integer(), db.ForeignKey('club_info.clubid')),
                        db.Column('tagid', db.Integer(), db.ForeignKey('tag_info.tagid')))

club_reviews = db.Table('club_reviews', 
                        db.Column('reviewid', db.Integer(), db.ForeignKey('review_info.reviewid')),
                        db.Column('clubid', db.Integer(), db.ForeignKey('club_info.clubid')))

# models
class Student(db.Model):
    __tablename__ = 'student_info'

    netid = db.Column(db.String(), primary_key = True)
    name = db.Column(db.String())
    res_college = db.Column(db.String())
    year = db.Column(db.String())
    major = db.Column(db.String())
    bio = db.Column(db.String())
    admin = db.Column(db.Boolean())
    blacklist = db.Column(db.Boolean())
    pictureURL = db.Column(db.String())
    pronouns = db.Column(db.String())
    linkedin = db.Column(db.String())
    instagram = db.Column(db.String())
    clubs = db.relationship("Club",
                                secondary=student_clubs)

    tags = db.relationship("Tag",
                                secondary=student_tags)

    reviews = db.relationship("Review",
                                secondary=student_reviews)

    def __init__(self, netid, name, res_college,
            year, major, bio, admin=False, pictureURL = None,
            pronouns = None, linkedin = None, instagram = None):
        self.netid = netid
        self.name = name
        self.res_college = res_college
        self.year = year
        self.major = major
        self.bio = bio
        self.admin= admin
        self.pictureURL = pictureURL
        self.pronouns = pronouns
        self.linkedin = linkedin
        self.instagram = instagram

    def __repr__(self):
        return self.netid

class Club(db.Model):
    __tablename__ = 'club_info'

    # auto-increment is automatic
    clubid = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    club_type = db.Column(db.String())
    diversity = db.Column(db.Float())
    inclusivity = db.Column(db.Float())
    time_commitment = db.Column(db.Float())
    experience_requirement = db.Column(db.Float())
    workload = db.Column(db.Float())
    pictureURL = db.Column(db.String())
    members = db.relationship("Student",
                               secondary=student_clubs)
    tags = db.relationship("Tag",
                               secondary=club_tags)
    reviews = db.relationship("Review",
                               secondary=club_reviews)

    @hybrid_property
    def combined(self):
        weighted = (0.2 * self.diversity + 0.2 * self.inclusivity + 
                    0.2 * self.time_commitment + 0.2 * self.workload + 
                    0.2 * self.experience_requirement)

        return (weighted)

    def __init__(self, name, description = None, club_type = None,
                diversity = 0, inclusivity = 0, time_commitment = 0,
                experience_requirement = 0, workload = 0):
        self.name = name
        self.description = description
        self.club_type = club_type
        self.diversity = 0
        self.inclusivity = 0
        self.time_commitment = 0
        self.workload = 0
        self.experience_requirement = 0

    def __repr__(self):
        return self.name

class Tag(db.Model):
    __tablename__ = 'tag_info'

    # auto-increment is automatic
    tagid = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String())

    students = db.relationship("Student",
                               secondary=student_tags)

    clubs = db.relationship("Club",
                               secondary=club_tags)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Rating_Period(db.Model):
    __tablename__ = "rating_period"

    id = db.Column(db.Integer(), primary_key = True)
    day = db.Column(db.Integer())
    month = db.Column(db.Integer())
    year = db.Column(db.Integer())

    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year
    
    def __repr__(self):
        return str(self.day) + " " + str(self.month) + " " + str(self.year)


class Review(db.Model):
    __tablename__ = 'review_info'

    # auto-increment is automatic
    reviewid = db.Column(db.Integer(), primary_key = True)
    diversity = db.Column(db.Integer())
    inclusivity = db.Column(db.Integer())
    time_commitment = db.Column(db.Integer())
    experience_requirement = db.Column(db.Integer())
    workload = db.Column(db.Integer())
    text_review = db.Column(db.Text())
    student = db.relationship("Student",
                               secondary=student_reviews,
                               post_update=True)
    club = db.relationship("Club",
                               secondary=club_reviews,
                               post_update=True)

    def __init__(self, diversity, inclusivity, time_commitment, experience_requirement, workload, text_review):
        self.diversity = diversity
        self.inclusivity = inclusivity
        self.time_commitment = time_commitment
        self.experience_requirement = experience_requirement
        self.workload = workload
        self.text_review = text_review

    def __repr__(self):
        str_review = "Club: " + str(self.club[0]) + '\n'
        str_review += 'Diversity: ' + str(self.diversity) + '\n'
        str_review += 'Inclusivity: ' + str(self.inclusivity) + '\n'
        str_review += 'Time Commitment: ' + str(self.time_commitment) + '\n'
        str_review += 'Experience required: ' + str(self.experience_requirement) + '\n'
        str_review += 'Workload: ' + str(self.workload) + '\n'
        str_review += "Text Review" + str(self.text_review) + "\n"

        return str_review

class Request(db.Model):
    __tablename__ = 'request_info'

    requestid = db.Column(db.Integer(), primary_key = True)
    request_type = db.Column(db.Integer())
    netid_sender = db.Column(db.String())
    netid_about = db.Column(db.String())
    clubid = db.Column(db.Integer())
    tagname = db.Column(db.String())
    description = db.Column(db.String())

    @hybrid_property
    def clubname(self):
        club = Club.query.filter_by(clubid=self.clubid).first()
        return club.name

    def __init__(self, request_type, netid_sender, netid_about = None, clubid = None, tagname = None, description = None):
        self.request_type = request_type
        self.netid_sender = netid_sender
        self.netid_about = netid_about
        self.clubid = clubid
        self.tagname = tagname
        self.description = description

    def __repr__(self):
        if self.request_type == DELETE_USER:
            club = Club.query.filter_by(clubid=self.clubid).first()
            clubname = club.name
            return ("Delete user " + str(self.netid_about) + " from " + str(clubname))
        
        elif self.request_type == BLACKLIST_USER:
            return ("Blacklist user " + str(self.netid_about))
        
        elif self.request_type == EDIT_USER:
            return("User " + str(self.netid_about) + " reported as inappropriate")

        elif self.request_type == EDIT_CLUB:
            club = Club.query.filter_by(clubid=self.clubid).first()
            clubname = club.name
            return("Club " + str(clubname) + " reported as inappropriate")

        else:
            return ("Add tag " + str(self.tagname))
            print(request)
            print(request.requestid)
            sen
