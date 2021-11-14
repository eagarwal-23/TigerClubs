from app import db
from models import Student, Club, Tag, Review, Request
DELETE_USER = 0
BLACKLIST_USER = 1
EDIT_USER = 2
EDIT_CLUB = 3
ADD_TAG = 4
# search database functions
def get_all_clubs():
    clubs = Club.query.all()
    return clubs
   
def get_all_tags():
    tags = Tag.query.all()
    return tags

def club_search(search):
    search_query = '%' + search + '%'
    clubs = Club.query.filter((Club.name.ilike(search_query) | Club.tags.any(Tag.name.ilike(search_query)))).all()
    # for club in clubs:
    #     print(club)
    return clubs

def student_search(search):
    search_query = "%" + search + "%"
    students = Student.query.filter(
        (Student.name.ilike(search_query)) |
        (Student.netid.ilike(search_query)) |
        (Student.res_college.ilike(search_query)) |
        (Student.year.ilike(search_query))
    ).all()

    return students

def filter_by_tags(tags):
    clubs = Club.query.filter(Club.tags.any(Tag.name.in_tags))
    return clubs

def get_all_requests():
    requests = Request.query.all()
    return requests

# obtaining and updating student profile information
# from the database
def get_student_info(netid):
    student = Student.query.filter_by(netid = netid).first()
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
    club = Club.query.filter_by(name = clubname).first()
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

def delete_review(reviewid):
    review = Review.query.filter_by(reviewid = reviewid).first()
    db.session.delete(review)

    db.session.commit()

def delete_student_club(netid, clubname):
    student = Student.query.filter_by(netid = netid).first()
    club = Club.query.filter_by(name = clubname).first()
    student.clubs.remove(club)
    club.members.remove(student)
    db.session.commit()

def delete_student_tag(netid, tagname): 
    student = Student.query.filter_by(netid = netid).first()
    tag = Tag.query.filter_by(name = tagname).first()
    student.tags.remove(tag)
    tag.students.remove(student)
    db.session.commit()

def delete_club_tag(clubname, tagname):
    club = Club.query.filter_by(name = clubname).first()
    tag = Tag.query.filter_by(name = tagname).first()
    club.tags.remove(tag)
    tag.clubs.remove(club)
    db.session.commit()

def blacklist_user(netid):
    student = Student.query.filter_by(netid = netid).first()
    student.blacklist = True
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

def add_request(request_type, netid_sender, netid_about = None, club = None, tagname = None):
    if request_type == "delete_user":
        request_type = DELETE_USER
        club = Club.query.filter_by(name = club).first()
        club = club.clubid
    elif request_type == "blacklist_user":
        request_type = BLACKLIST_USER  
    elif request_type == "edit_user":
        request_type = EDIT_USER
    if request_type == "edit_club":
        club = Club.query.filter_by(name = club).first()
        club = club.clubid
        request_type = EDIT_CLUB
    elif request_type == "add_tag":
        request_type = ADD_TAG
    request = Request(request_type, netid_sender, netid_about, club, tagname)
    db.session.add(request)
    db.session.commit()

def blacklist_student(netid):
    student = get_student_info(netid)
    student.blacklist = True
    db.session.commit()

def get_request_info(requestid):
    request = Request.query.filter_by(requestid = requestid).first()
    return request

def delete_request(requestid):
    request = get_request_info(requestid)
    db.session.delete(request)
    db.session.commit()
