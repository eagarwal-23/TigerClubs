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
def club_search(search, query = 'Overall', page = 1):
    search_query = '%' + search + '%'
    clubs = Club.query.filter((Club.name.ilike(search_query) | Club.tags.any(Tag.name.ilike(search_query))))
    if query == 'Overall':
        clubs = clubs.order_by(Club.ranking_over)
    elif query == 'Diversity':
        clubs = clubs.order_by(Club.ranking_div)
    elif query == 'Inclusivity':
        clubs = clubs.order_by(Club.ranking_inc)
    elif query == 'Time Commitment':
        clubs = clubs.order_by(Club.ranking_time)
    elif query == 'Workload':
        clubs = clubs.order_by(Club.ranking_work)
    elif query == 'Experience Requirement':
        clubs = clubs.order_by(Club.ranking_exp)
    elif query == 'Club Name':
        clubs = clubs.order_by(Club.name)

    clubs = clubs.paginate(page = page, per_page = 20)
    return clubs

# sort list of Clubs on page by chosen criteria
def admin_club_search(search, page = 1):
    search_query = '%' + search + '%'
    clubs = Club.query.filter((Club.name.ilike(search_query) | Club.tags.any(Tag.name.ilike(search_query))))
    clubs = clubs.order_by(Club.name).paginate(page = page, per_page = 20)
    return clubs

def calculate_over():
    print("recalculating overall")
    # overall
    clubs = Club.query.order_by(Club.combined.desc()).all()
    for i in range(len(clubs)):
        club = clubs[i]
        club.ranking_over = i + 1
        db.session.add(club)    
    db.session.commit()
    print("done")

def calculate_div():
    print("recalculating div")
    # diversity
    clubs = Club.query.order_by(Club.diversity.desc()).all()
    for i in range(len(clubs)):
        club = clubs[i]
        club.ranking_div = i + 1
        db.session.add(club)    
    db.session.commit()
    print("done")

def calculate_inc():
    print("recalculating inc")
    # diversity
    clubs = Club.query.order_by(Club.inclusivity.desc()).all()
    for i in range(len(clubs)):
        club = clubs[i]
        club.ranking_inc = i + 1
        db.session.add(club)    
    db.session.commit()
    print("done")

def calculate_time():
    print("recalculating time")
    # diversity
    clubs = Club.query.order_by(Club.time_commitment.desc()).all()
    for i in range(len(clubs)):
        club = clubs[i]
        club.ranking_time = i + 1
        db.session.add(club)    
    db.session.commit()
    print("done")

def calculate_work():
    print("recalculating work")
    # diversity
    clubs = Club.query.order_by(Club.workload.desc()).all()
    for i in range(len(clubs)):
        club = clubs[i]
        club.ranking_work = i + 1
        db.session.add(club)    
    db.session.commit()
    print("done")

def calculate_exp():
    print("recalculating exp")
    # diversity
    clubs = Club.query.order_by(Club.experience_requirement.desc()).all()
    for i in range(len(clubs)):
        club = clubs[i]
        club.ranking_exp = i + 1
        db.session.add(club)    
    db.session.commit()
    print("done")

def calculate_club_rankings():
    print("recalculating rankings")
    print("lalalalala")
    # overall
    clubs = Club.query.order_by(Club.combined.desc()).all()
    for i in range(len(clubs)):
        club = clubs[i]
        club.ranking_over = i + 1

    # diversity
    clubs = Club.query.order_by(Club.diversity.desc()).all()
    for i in range(len(clubs)):
        club = clubs[i]
        club.ranking_div = i + 1

    # inclusivity
    clubs = Club.query.order_by(Club.inclusivity.desc()).all()
    for i in range(len(clubs)):
        club = clubs[i]
        club.ranking_inc = i + 1
    
    # time commitment
    clubs = Club.query.order_by(Club.time_commitment.desc()).all()
    for i in range(len(clubs)):
        club = clubs[i]
        club.ranking_time = i + 1

    # workload
    clubs = Club.query.order_by(Club.workload.desc()).all()
    for i in range(len(clubs)):
        club = clubs[i]
        club.ranking_work = i + 1

    # experience requirement
    clubs = Club.query.order_by(Club.experience_requirement.desc()).all()
    for i in range(len(clubs)):
        club = clubs[i]
        club.ranking_exp = i + 1
        db.session.add(club)    
    db.session.commit()