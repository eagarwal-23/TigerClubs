from app import db
from models import Student, Club, Tag, Review

# get Student object given netid
def get_student_info(netid):
    student = Student.query.filter_by(netid = netid).first()
    return student

def update_student_photo(netid, pictureURL = None):
    student = Student.query.filter_by(netid = netid).first()
    if pictureURL != "" and pictureURL:
        student.pictureURL = pictureURL
    db.session.commit()

# edit Student's information given their netid
def update_student_info(netid, bio = None, clubs = None, tags = None, instagram = None, linkedin = None):
    student = Student.query.filter_by(netid = netid).first()
    if bio != "" and bio:
        student.bio = bio

    if clubs != "" and clubs:
        for oneClub in clubs:
            club = Club.query.filter_by(name=oneClub).first()
            print(club)
            student.clubs.append(club)
            db.session.add(student)

    if tags != "" and tags:
        for oneTag in tags:
            tag = Tag.query.filter_by(name=oneTag).first()
            print(tag)
            student.tags.append(tag)
            db.session.add(student)
    
    if instagram != "" and not None:
        student.instagram = instagram

    if linkedin != "" and not None:
        student.linkedin = linkedin


    db.session.commit()

# for student ratings page

# get all ratings for a Student given their netid
def get_student_ratings(netid):
    student = Student.query.filter_by(netid = netid).first()
    reviews = student.reviews
    return reviews

# add rating from Student with netid for club with name club
# and ratings div, inc, time, exp, and work
def add_rating(netid, clubname, diversity, inclusivity, time_commitment, experience_requirement, workload, text_review):
    student = Student.query.filter_by(netid = netid).first()
    club = Club.query.filter_by(name = clubname).first()
    review = Review(diversity, inclusivity, time_commitment, experience_requirement, workload, text_review)
    student.reviews.append(review)
    club.reviews.append(review)
    db.session.add(review)
    db.session.commit()

def edit_rating(reviewid, diversity, inclusivity, time_commitment, experience_requirement, workload, text_review):
    review = Review.query.filter_by(reviewid = reviewid).first()
    review.diversity = diversity
    review.inclusivity = inclusivity
    review.time_commitment = time_commitment
    review.workload = workload
    review.experience_requirement = experience_requirement
    review.text_review = text_review
    db.session.add(review)
    db.session.commit()

def delete_rating(reviewid):
    review = Review.query.filter_by(reviewid = reviewid).first()
    db.session.delete(review)
    db.session.commit()

def blacklist_student(netid):
    student = Student.query.filter_by(netid = netid).first()
    student.blacklist = True
    db.session.commit()

def whitelist_student(netid):
    student = Student.query.filter_by(netid = netid).first()
    student.blacklist = False
    db.session.commit()

def get_unrated_clubs(netid):
    student = Student.query.filter_by(netid = netid).first()
    clubs = student.clubs
    reviews = student.reviews
    rated = []
    unrated = []
    for review in reviews:
        club = review.club
        rated.append(club[0])
    for club in clubs:
        if club not in rated:
            unrated.append(club)
    return unrated