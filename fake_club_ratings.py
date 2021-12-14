from datetime import time
from app import db
from models import Club, Student, Tag, Review
import pandas as pd
import random
from random import choices
import lorem
from db_club_profile import calculate_all_club_ratings, calculate_club_rating

EXISTING_CLUBS = [1, 2, 5, 6, 8, 10, 11, 12, 13, 15, 16, 27]
NUM_MEMBERS = 25

def remove_all_reviews(clubname):
    club = Club.query.filter_by(name = clubname).first()
    reviews = club.reviews
    new_reviews = []
    club.reviews = new_reviews
    db.session.add(club)
    for review in reviews:
        reviewThis = Review.query.filter_by(reviewid = review.reviewid).first()
        db.session.delete(reviewThis)
    db.session.commit()

def add_rating(netid, clubname, diversity, inclusivity, time_commitment, experience_requirement, workload, text_review):
    student = Student.query.filter_by(netid = netid).first()
    club = Club.query.filter_by(name = clubname).first()
    review = Review(diversity, inclusivity, time_commitment, experience_requirement, workload, text_review)
    student.reviews.append(review)
    club.reviews.append(review)
    db.session.add(review)
    db.session.commit()

def get_all_clubs():
    clubs = Club.query.all()
    return clubs

def get_all_students():
    students = Student.query.all()
    return students

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

def delete_added_clubs():
    clubs = get_all_clubs()
    for club in clubs:
        clubid = club.clubid
        if not clubid in EXISTING_CLUBS:
            db.session.delete(club)
    db.session.commit()

STUDENTS = ['eagarwal', 'jg41', 'nreptak', 'camilanv',
            'nadiar', 'ajguerra']

if __name__ == "__main__":
    n_students = 50
    n_members = 10
    # students = get_all_netids()
    # selected_students = (random.sample(students, n_students))
    # #print(selected_students)
    # students = selected_students + STUDENTS

    # # list of 100 random students + 5 of us
    # eesha = Student.query.filter_by(netid='eagarwal').first()
    # camila = Student.query.filter_by(netid='camilanv').first()
    # natalie = Student.query.filter_by(netid='nreptak').first()
    # nadia = Student.query.filter_by(netid='nadiar').first()
    # anthony = Student.query.filter_by(netid='ajguerra').first()
    # josh = Student.query.filter_by(netid='jg41').first()

    # students.append(eesha)
    # students.append(camila)
    # students.append(nadia)
    # students.append(natalie)
    # students.append(anthony)
    # students.append(josh)

    # members = random.sample(students, n_members)
    # #print(members)
    # clubs = get_all_clubnames()
    # club = clubs[0]
    # add_students_club(members, club)

    clubs = get_all_clubs()
    students = get_all_students()
    
    # adding n_members randomly-selected students to all clubs
    for club in clubs:
        print(club.members)
        members = random.sample(students, n_members)
        add_students_club(members, club.name)

    # adding 5 randomly generated ratings to all clubs
    ratings = [1, 2, 3, 4, 5]
    weights = [0.05, 0.05, 0.2, 0.35, 0.35]
    for club in clubs:
        members = club.members
        for i in range(5):
            if members == []:
                selected_students = (random.sample(students, NUM_MEMBERS))
                add_students_club(selected_students, club.clubname)
            student = members[i]
            diversity = (choices(ratings, weights))[0]
            inclusivity = (choices(ratings, weights))[0]
            time_commitment = (choices(ratings, weights))[0]
            experience_requirement = (choices(ratings, weights))[0]
            workload = (choices(ratings, weights))[0]
            text = lorem.paragraph()
            add_rating(student.netid, club.name, diversity,
                        inclusivity, time_commitment, experience_requirement,
                        workload, text)
        calculate_club_rating(club.name)
        print("Done with", club.name)