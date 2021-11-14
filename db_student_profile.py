from app import db
from models import Student, Club, Tag, Review

# get Student object given netid
def get_student_info(netid):
    student = Student.query.filter_by(netid = netid).first()
    return student

# edit Student's information given their netid
def update_student_info(netid, bio = None, clubs = None, tags = None):
    student = Student.query.filter_by(netid = netid).first()
    if bio != "" and bio is not None:
        student.bio = bio

    if clubs != "" and clubs is not None:
        club = Club.query.filter_by(name=clubs).first()
        student.clubs.append(club)
        db.session.add(student)

    if tags != "" and tags is not None:
        tag = Tag.query.filter_by(name=tags).first()
        student.tags.append(tag)
        db.session.add(student)

    db.session.commit()

# for student ratings page

# get all ratings for a Student given their netid
def get_student_ratings(netid):
    student = Student.query.filter_by(netid = netid).first()
    reviews = student.reviews
    return reviews

# add rating from Student with netid for club with name club
# and ratings div, inc, time, exp, and work
def add_rating(netid, clubname, diversity, inclusivity, time_commitment, experience_requirement, workload):
    student = Student.query.filter_by(netid = netid).first()
    club = Club.query.filter_by(name = clubname).first()
    review = Review(diversity, inclusivity, time_commitment, experience_requirement, workload)
    student.reviews.append(review)
    club.reviews.append(review)
    db.session.add(review)
    db.session.commit()

def delete_rating(reviewid):
    review = Review.query.filter_by(reviewid = reviewid).first()
    db.session.delete(review)
    db.session.commit()
