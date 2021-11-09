from app import db
from models import Student, Club, Tag, Review

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