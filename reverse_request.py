from app import db
from models import Student, Club, Tag, Review, Request

from db1 import *
DELETE_USER = 0
BLACKLIST_USER = 1
EDIT_USER = 2
EDIT_CLUB = 3
ADD_TAG = 4

def add_student_club(netid, clubname):
    student = get_student_info(netid)
    club = Club.query.filter_by(name = clubname).first()
    club.members.append(student)
    student.clubs.append(club)
    db.session.add(student)
    db.session.commit()

def rev_blacklist_student(netid):
    student = Student.query.filter_by(netid = netid).first()
    student.blacklist = False
    db.session.commit()

if __name__ == "__main__":
    add_request(request_type="delete_user", netid_sender="eagarwal", netid_about="ajguerra", club = "SWE")
    add_request(request_type="edit_user", netid_sender="eagarwal", netid_about="ajguerra")
    add_request(request_type="edit_club", netid_sender="ajguerra", club = "PWICS")
    add_request(request_type="blacklist_user", netid_sender="ajguerra", netid_about="eagarwal")
    add_request(request_type="add_tag", netid_sender="ajguerra", tagname="Plants")

    add_student_club('ajguerra', 'SWE')
    rev_blacklist_student('eagarwal')
    
