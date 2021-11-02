from app import db
from models import Student, Club, Tag, Review

from db1 import student_search

def club_search(search):
    clubs = None
    search_query = '%' + search + '%'
    clubs = Club.query.filter((Club.name.ilike(search_query) | Club.tags.any(Tag.name.ilike(search_query)))).all()
    for club in clubs:
        print(club)

<<<<<<< Updated upstream
=======
def add_tag(name):
    tag = Tag(name)
    db.session.add(tag)
    db.session.commit()



>>>>>>> Stashed changes
if __name__ == "__main__":
    # add_tag('Instruments')
    # add_tag('Movies')
    # add_tag('MCU')
    # add_tag('Baseball')
    # add_tag('Basketball')
    # add_tag('Beachball')
    # add_tag('Sports')
    # add_tag('Bowling')
    # add_tag('Cricket')

    student = Student.query.filter_by(netid = 'eagarwal').first()
    reviews = student.reviews
    for review in reviews:
        print(review)

    # search = 'a'
    # student_search('a')
