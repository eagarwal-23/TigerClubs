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
    tags = Tag.query.order_by(Tag.name).all()
    return tags

# get list of all tag names in tag_info table  
def get_all_tagnames():
    tags = Tag.query.order_by(Tag.name).all()
    final = list()
    for tag in tags:
        final.append(tag.name)
    return final

# get list of all Club objects whose name or tags
# match search query
# def club_search(search):
#     search_query = search + '%'
#     clubs = Club.query.filter((Club.name.ilike(search_query) | Club.tags.any(Tag.name.ilike(search_query)))).all()
#     return clubs

# get a list of all Student objects whose name, netid, 
# res college, or year matches search query
def student_search(search, pagenum, per_page):
    search_query = '%' + search + "%"
    students = Student.query.filter(
        (Student.name.ilike(search_query)) |
        (Student.netid.ilike(search_query)) |
        (Student.res_college.ilike(search_query)) |
        (Student.year.ilike(search_query))
    ).order_by(Student.name).paginate(page = pagenum, per_page = per_page)

    return students

def tag_search(search):
    search_query = '%' + search + "%"
    tags = Tag.query.filter((Tag.name.ilike(search_query))).order_by(Tag.name).all()
    return tags

# get all Club objects associated with any tag in 
# input list of tags
def filter_by_tags(tags):
    clubs = Club.query.filter(Club.tags.any(Tag.name.in_(tags))).all()
    return clubs

# sort list of Clubs on page by chosen criteria
def club_search(search, query = 'Overall', tags = get_all_tagnames(), page = 1):
    search_query = '%' + search + '%'
    clubs = Club.query.filter(Club.tags.any(Tag.name.in_(tags)),
                             (Club.name.ilike(search_query) | Club.tags.any(Tag.name.ilike(search_query))))
    if query == 'Overall':
        clubs = clubs.order_by(Club.combined.desc())
    elif query == 'Diversity':
        clubs = clubs.order_by(Club.diversity.desc())
    elif query == 'Inclusivity':
        clubs = clubs.order_by(Club.inclusivity.desc())
    elif query == 'Time Commitment':
        clubs = clubs.order_by(Club.time_commitment.desc())
    elif query == 'Workload':
        clubs = clubs.order_by(Club.workload.desc())
    elif query == 'Experience Requirement':
        clubs = clubs.order_by(Club.experience_requirement.desc())
    elif query == 'Club Name':
        clubs = clubs.order_by(Club.name)

    clubs = clubs.paginate(page = page, per_page = 20)
    return clubs

# sort list of Clubs on page by chosen criteria
def admin_club_search(search, query = 'Overall', tags = get_all_tagnames(), page = 1):
    search_query = '%' + search + '%'
    clubs = Club.query.filter(Club.tags.any(Tag.name.in_(tags)),
                             (Club.name.ilike(search_query) | Club.tags.any(Tag.name.ilike(search_query))))
    clubs = clubs.order_by(Club.name).paginate(page = page, per_page = 20)
    return clubs