from app import db
from db_search import get_all_clubs
from db_student_profile import get_student_info
from models import Student, Club, Tag, Review, Request

DELETE_USER = 0
BLACKLIST_USER = 1
EDIT_USER = 2
EDIT_CLUB = 3
ADD_TAG = 4

# get list of all Request objects in request_info table
def get_all_requests():
    requests = Request.query.all()
    return requests

# add Request object to request_info table
def add_request(request_type, netid_sender, netid_about = None, 
                club = None, tagname = None, descrip = None):
    if request_type == "delete_user":
        request_type = DELETE_USER
        club = Club.query.filter_by(name = club).first()
        if (club == None or get_student_info(netid_about) == None):
            return None
        club = club.clubid
        request = Request(request_type, netid_sender, netid_about, club, None, description= descrip)
    elif request_type == "blacklist_user":
        request_type = BLACKLIST_USER
        if (get_student_info(netid_about) == None):
            return None
        request = Request(request_type, netid_sender, netid_about, None, None, description = descrip)
    elif request_type == "edit_user":
        request_type = EDIT_USER
        if (get_student_info(netid_about) == None):
            return None
        request = Request(request_type, netid_sender, netid_about, None, None, description = descrip)
    if request_type == "edit_club":
        club = Club.query.filter_by(name = club).first()
        if (club == None):
            return None
        club = club.clubid
        request_type = EDIT_CLUB
        request = Request(request_type, netid_sender, None, club, None, description = descrip)
    elif request_type == "add_tag":
        request_type = ADD_TAG
        request = Request(request_type, netid_sender, None, None, tagname, description = descrip)
    
    db.session.add(request)
    db.session.commit()
    return 0

# get Request object given requestid
def get_request_info(requestid):
    request = Request.query.filter_by(requestid = requestid).first()
    return request

# delete Request from request_info table given requestid
def delete_request(requestid):
    request = get_request_info(requestid)
    db.session.delete(request)
    db.session.commit()

# for DELETE_USER type request
def delete_student_club(netid, clubid):
    student = Student.query.filter_by(netid = netid).first()
    club = Club.query.filter_by(clubid = clubid).first()
    student.clubs.remove(club)
    print(student.clubs)
    db.session.commit()

# for BLACKLIST_USER type request
def blacklist_student(netid):
    student = Student.query.filter_by(netid = netid).first()
    student.blacklist = True
    print(student)
    db.session.commit()

# for EDIT_USER type request => db functions in db_student_profile.py
# for EDIT_CLUB type request => db functions in db_club_profile.py

# for ADD_TAG type request
def add_tag_db(tagname):
    tag = Tag(tagname)
    db.session.add(tag)
    db.session.commit()

# for admin students tab
def add_student(netid, name, res_college, year, major, bio = "", admin = False, pictureURL = None):
    # what should we do if we delete student and then we want to repopulate 
    # our users, probably keep list of users we deleted so we can make
    # sure we don't recreate them
    if (get_student_info(netid) != None):
        print(netid, " already exists")
        return
    student = Student(netid, name, res_college, year, major, bio, admin, pictureURL)
    db.session.add(student)
    db.session.commit()

def delete_student(netid, name, res_college, year, major, bio, admin = False, pictureURL = None):
    student = Student(netid, name, res_college, year, major, bio, admin, pictureURL)
    db.session.delete(student)
    db.session.commit()

def delete_student_tag(netid, tagname): 
    student = Student.query.filter_by(netid = netid).first()
    tag = Tag.query.filter_by(name = tagname).first()
    student.tags.remove(tag)
    tag.students.remove(student)
    db.session.commit()

# for admin clubs tab
def add_club(name, description):
    club = Club(name, description)
    db.session.add(club)
    db.session.commit()

def delete_club_db(clubid):
    club = Club.query.filter_by(clubid = clubid).first()
    db.session.delete(club)
    db.session.commit()

def delete_club_tag(clubname, tagname):
    club = Club.query.filter_by(name = clubname).first()
    tag = Tag.query.filter_by(name = tagname).first()
    club.tags.remove(tag)
    tag.clubs.remove(club)
    db.session.commit()

def delete_tag_db(tagname):
    tag = Tag.query.filter_by(name = tagname).first()
    db.session.delete(tag)
    db.session.commit()

def edit_tag_db(tagid, newtagname):
    tag = Tag.query.filter_by(tagid = tagid).first()
    tag.name = newtagname
    db.session.commit()

def delete_tag_db_id(tagid):
    tag = Tag.query.filter_by(tagid = tagid).first()
    db.session.delete(tag)
    db.session.commit()

    
