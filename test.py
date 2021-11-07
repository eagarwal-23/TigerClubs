from app import db
from models import Student, Club, Tag, Review

from db1 import get_student_ratings, student_search, update_club_info

def club_search(search):
    clubs = None
    search_query = '%' + search + '%'
    clubs = Club.query.filter((Club.name.ilike(search_query) | Club.tags.any(Tag.name.ilike(search_query)))).all()
    for club in clubs:
        print(club)

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
    # student.reviews.remove(review)
    # club.reviews.remove(review)
    db.session.commit()

if __name__ == "__main__":
    #add_review("eagarwal", "Roaring 20", 5, 4, 3, 4, 5)
    delete_review("eagarwal", "Roaring 20", 21)

    # add_tag('Beachball')
    # add_tag('Sports')
    # add_tag('Bowling')
    # add_tag('Cricket')

    # student = Student.query.filter_by(netid = 'eagarwal').first()
    # reviews = student.reviews
    # for review in reviews:
    #     print(review)

    # club = Club.query.filter_by(clubid = "3").first()
    # reviews = club.reviews

    # for review in reviews:
    #     print(review.inclusivity)

    # ratings = get_student_ratings("eagarwal")
    # print(ratings)

    # search = 'a'
    # student_search('a')

    # update_club_info(name = 'Princeton Mock Trial', tags = 'Public-speaking, Bowling, Sports, Instruments, Dogs, Cats')