from models import Student, Club, Tag
from app import db

def get_student_info(netid):
    student = Student.query.filter_by(netid = netid).first()
    return student

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
        
def get_club_info(clubname):
    club = Club.query.filter(Club.name.like(clubname)).first()
    return club

def get_clubs(input):
    #doesn't work if not right case
    clubs = Club.query.filter(Club.name.contains("%" + input + "%"))
    #clubs2 = Club.query.filter(Club.tags.contains("%" + input + "%"))
    #allclubs.append(clubs)
    #allclubs.append(clubs2)
    print(clubs)
    return clubs


def update_club_info(name, description = None, members = None, tags = None):
    club = Club.query.filter_by(name = name).first()
    if description != "" and not None:
        club.description = description
    
    if members != "" and members is not None:
        student = Student.query.filter_by(name=members).first()
        club.members.append(student)
        db.session.add(club)

    if tags != "" and tags is not None:
        tag = Tag.query.filter_by(name=tags).first()
        club.tags.append(tag)
        db.session.add(club)

    db.session.commit()

