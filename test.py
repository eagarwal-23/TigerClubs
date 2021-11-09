from app import db
from models import Student, Club, Tag, Review

from db1 import get_student_ratings, student_search, update_club_info

def club_search(search):
    clubs = None
    search_query = '%' + search + '%'
    clubs = Club.query.filter((Club.name.ilike(search_query) | Club.tags.any(Tag.name.ilike(search_query)))).all()
    for club in clubs:
        print(club)

def filter_by_tags(tags):
    clubs = Club.query.filter(Club.tags.any(Tag.name.in_(tags))).all()
    return clubs

def get_all_clubs():
    clubs = Club.query.all()
    return clubs
    
def get_all_tags():
    tags = Tag.query.all()
    return tags

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
        #tags = tags.split(',')
        for tag in tags:
            tag = tag.strip()
            tag = Tag.query.filter_by(name=tag).first()
            club.tags.append(tag)
            db.session.add(club)

    db.session.commit()

if __name__ == "__main__":
    #add_review("eagarwal", "Roaring 20", 5, 4, 3, 4, 5)
    # delete_review("eagarwal", "Roaring 20", 21)
    # update_club_info("Roaring 20", tags = ("Dogs", "Coding", "SQL", "MCU", "Bowling", "Innovation"))
    # update_club_info("Nassoons", tags = ("Dogs", "Coding", "SQL", "MCU", "Bowling", "Innovation"))
    # update_club_info("eXpressions", tags = ("Dogs", "Coding", "SQL", "MCU", "Bowling", "Innovation"))
    # update_club_info("SWE", tags = ("Dogs", "Coding", "SQL", "MCU", "Bowling", "Innovation"))
    # update_club_info("PWICS", tags = ("Dogs", "Coding", "SQL", "MCU", "Bowling", "Innovation"))

    # clubs = filter_by_tags(["Dogs", "League of Legends", "Coding"])
    # print(clubs)
    clubs = get_all_clubs()
    for club in clubs:
        print(club)

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