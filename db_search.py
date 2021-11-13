from app import db
from models import Student, Club, Tag

# get list of all Student objects in student_info table
def get_all_students():
    students = Student.query.all()
    return students

# get list of all Club objects in club_info table
def get_all_clubs():
    clubs = Club.query.all()
    return clubs
 
# get list of all Tag objects in tag_info table  
def get_all_tags():
    tags = Tag.query.all()
    return tags

# get list of all Club objects whose name or tags
# match search query
def club_search(search):
    search_query = '%' + search + '%'
    clubs = Club.query.filter((Club.name.ilike(search_query) | Club.tags.any(Tag.name.ilike(search_query)))).all()
    return clubs

# get a list of all Student objects whose name, netid, 
# res college, or year matches search query
def student_search(search):
    search_query = "%" + search + "%"
    students = Student.query.filter(
        (Student.name.ilike(search_query)) |
        (Student.netid.ilike(search_query)) |
        (Student.res_college.ilike(search_query)) |
        (Student.year.ilike(search_query))
    ).all()

    return students

# get all Club objects associated with any tag in 
# input list of tags
def filter_by_tags(tags):
    clubs = Club.query.filter(Club.tags.any(Tag.name.in_tags))
    return clubs

# sort list of Clubs on page by chosen criteria
def sort_by(clubs, query):
    pass