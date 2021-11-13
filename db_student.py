from app import db
from models import Student

# get student information for a
# given netid
def get_student_info(netid):
    student = Student.query.filter_by(netid = netid).first()
    return student

# get a particular students
# provided reviews
def get_student_ratings(netid):
    student = Student.query.filter_by(netid = netid).first()
    reviews = student.reviews
    return reviews

# update info (bio, clubs, interests) for a
# student with a given netid
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