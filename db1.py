from app import db
from models import Student, Club, Tag, Review

# obtaining and updating student profile information
# from the database
def get_student_info(netid):
    print("in function, netid =", netid)
    student = Student.query.filter_by(netid = netid).first()
    print("stu is :", student)
    return student

def get_student_ratings(netid):
    student = Student.query.filter_by(netid = netid).first()
    reviews = student.reviews
    return reviews

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

def add_student_rating(netid, club, div, inc, time, exp, work):
    try:
        student = get_student_info(netid)
        clubname = club.strip()
        club = Club.query.filter_by(name = clubname).first()

        review = Review(div, inc, time, exp, work)
        review.club.append(club)
        review.student.append(student)
        db.session.add(review)

        print(review.reviewid)
        db.session.commit()
    except Exception as e:
        print(e)
        
# obtaining and updating club profile information
# from the database
def get_club_info(clubname):
    club = Club.query.filter(Club.name.like(clubname)).first()
    return club

def update_club_info(name, description = None, members = None, tags = None):
    club = Club.query.filter_by(name = name).first()

    if description != "" and not None:
        club.description = description
    
    if members != "" and members is not None:
        members = members.split(',')
        for member in members:
            member = member.strip()

            student = Student.query.filter_by(name=member).first()
            club.members.append(student)
            db.session.add(club)

    if tags != "" and tags is not None:
        tags = tags.split(',')
        for tag in tags:
            tag = tag.strip()
            tag = Tag.query.filter_by(name=tag).first()
            club.tags.append(tag)
            db.session.add(club)

    db.session.commit()

def get_club_ratings(clubid):
    club = Club.query.filter_by(clubid = clubid).first()
    reviews = club.reviews
    return reviews

def add_tag(name):
    tag = Tag(name)
    db.session.add(tag)
    db.session.commit()

def add_club(name, description):
    club = Club(name, description)
    db.session.add(club)
    db.session.commit()

def add_student(netid, name, res_college, year, major, bio, admin = False):
    student = Student(netid, name, res_college, year, major, bio, admin)
    db.session.add(student)
    db.session.commit()

def add_review(netid, clubname, diversity, inclusivity, time_commitment, experience_requirement, workload):
    student = Student.query.filter_by(netid = netid).first()
    club = Club.query.filter_by(name = clubname).first()
    review = Review(diversity, inclusivity, time_commitment, experience_requirement, workload)
    student.reviews.append(review)
    club.reviews.append(review)
    db.session.add(review)
    db.session.commit()

def delete_tag(name):
    tag = Tag(name)
    db.session.delete(tag)
    db.session.commit()

def delete_club(name, description):
    club = Club(name, description)
    db.session.delete(club)
    db.session.commit()

def delete_student(netid, name, res_college, year, major, bio, admin = False):
    student = Student(netid, name, res_college, year, major, bio, admin)
    db.session.delete(student)
    db.session.commit()

def delete_review(netid, clubname, reviewid):
    student = Student.query.filter_by(netid = netid).first()
    club = Club.query.filter_by(name = clubname).first()
    review = Review.query.filter_by(reviewid = reviewid).delete()
    student.reviews.remove(review)
    club.reviews.remove(review)
    db.session.commit()

def calculate_all_club_ratings():
    clubs = get_all_clubs()
    for club in clubs:
        reviews = get_club_ratings(club.clubid)
        print(reviews)

        diversity = 0.0
        inclusivity = 0.0
        time_commitment = 0.0
        workload = 0.0
        experience_requirement = 0.0
        counter = 0

        for review in reviews:
            diversity += review.diversity
            inclusivity += review.inclusivity
            time_commitment += review.time_commitment
            workload += review.workload
            experience_requirement += review.experience_requirement
            counter += 1
        
        diversity /= counter
        inclusivity /= counter
        time_commitment /= counter
        workload /= counter
        experience_requirement /= counter

        club.diversity = diversity
        club.inclusivity = inclusivity
        club.time_commitment = time_commitment
        club.experience_requirement = experience_requirement
        club.workload = workload
