from app import db
from models import Student, Club, Tag

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

def club_search(search):
    search_query = '%' + search + '%'
    clubs = Club.query.filter((Club.name.ilike(search_query) | Club.tags.any(Tag.name.ilike(search_query)))).all()
    for club in clubs:
        print(club)
    return clubs

def student_search(search):
    search_query = "%" + search + "%"
    students = Student.query.filter(
        (Student.name.ilike(search_query)) |
        (Student.netid.ilike(search_query)) |
        (Student.res_college.ilike(search_query)) |
        (Student.year.ilike(search_query))
    ).all()

    print(students)
    return students

def get_student_ratings(netid):
    student = Student.query.filter_by(netid = netid).first()
    reviews = student.reviews
    return reviews

def add_student_rating(netid, club, div, inc, time, exp, work):
    student = get_student_info(netid)
    club = get_club_info(club)

    review = Review(div, inc, time, exp, work)
    review.student = student
    review.club = club

    db.session.add(review)
    db.session.commit()


def get_club_ratings(clubid):
    club = Club.query.filter_by(clubid = clubid).first()
    reviews = club.reviews
    return reviews
