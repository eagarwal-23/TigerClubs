from app import db
from fake_club_ratings import add_students_club
from models import Club, Student, Tag, Review, Request
import pandas as pd
import random

EXISTING_CLUBS = [1, 2, 5, 6, 8, 10, 11, 12, 13, 15, 16, 27]

def get_all_students():
    students = Student.query.all()
    return students

def get_all_clubs():
    clubs = Club.query.all()
    return clubs

def add_club(name, description, club_type, diversity = 0, 
    inclusivity = 0, time_commitment = 0,
    experience_requirement = 0, workload = 0):
    club = Club(name, description, club_type, diversity, 
                inclusivity, time_commitment, experience_requirement, 
                workload)
    club.diversity = 0
    club.inclusivity = 0
    club.time_commitment = 0
    club.experience_requirement = 0
    club.workload = 0
    db.session.add(club)
    db.session.commit()

def tag_in_db(tagname):
    this_tag = Tag.query.filter_by(name = tagname).first()
    all_tags = Tag.query.all()
    return (this_tag in all_tags)

def club_in_db(clubname):
    this_club = Club.query.filter_by(name = clubname).first()
    all_clubs = Club.query.all()
    return (this_club in all_clubs)

def add_tag(tagname):
    tag = Tag(tagname)
    db.session.add(tag)
    db.session.commit()

def add_tags_club(tagnames, clubname):
    club = Club.query.filter_by(name = clubname).first()
    for tagname in tagnames:
        if tag_in_db(tagname):
            tag = Tag.query.filter_by(name = tagname).first()
        else:
            tag = Tag(name = tagname)
        club.tags.append(tag)
        db.session.add(club)
    db.session.commit()

def add_students_club(students, clubname):
    club = Club.query.filter_by(name = clubname).first()
    for student in students:
        club.members.append(student)
        db.session.add(club)
    db.session.commit()

def remove_all_members(clubname):
    club = Club.query.filter_by(name = clubname).first()
    new_members = []
    club.members = new_members
    db.session.add(club)
    db.session.commit()

def remove_all_tags(clubname):
    club = Club.query.filter_by(name = clubname).first()
    new_tags = []
    club.tags = new_tags
    db.session.add(club)
    db.session.commit()

def get_all_club_requests(clubid):
    requests = Request.query.filter_by(clubid = clubid).all()
    return requests

def delete_club_db(clubid):
    club = Club.query.filter_by(clubid = clubid).first()
    list_of_reviews = club.reviews
    list_of_requests = get_all_club_requests(club.clubid)
    db.session.delete(club)
    for review in list_of_reviews:
        reviewThis = Review.query.filter_by(reviewid = review.reviewid).first()
        db.session.delete(reviewThis)
    for request in list_of_requests:
        requestThis = Request.query.filter_by(requestid = request.requestid).first()
        db.session.delete(requestThis)
    db.session.commit()

def delete_added_clubs():
    clubs = get_all_clubs()
    for club in clubs:
        clubid = club.clubid
        delete_club_db(clubid)
    db.session.commit()