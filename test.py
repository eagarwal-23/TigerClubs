from app import db
from models import Student, Club, Tag, Review

from db1 import get_student_ratings, student_search, update_club_info, get_club_ratings

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

    def calculate_all_club_ratings():
        clubs = get_all_clubs()
        for club in clubs:
            reviews = get_club_ratings(club.clubid)
            print(reviews)

            diversity = 0.0
            inclusivity = 0.0
            time_commitment = 0.0
            workload = 0.0
            experience_requirement = 0.0
            counter = 0

            for review in reviews:
                diversity += review.diversity
                inclusivity += review.inclusivity
                time_commitment += review.time_commitment
                workload += review.workload
                experience_requirement += review.experience_requirement
                counter += 1
            
            if diversity != 0:
                diversity /= counter
                inclusivity /= counter
                time_commitment /= counter
                workload /= counter
                experience_requirement /= counter
            else:
                diversity = inclusivity = time_commitment = workload =experience_requirement = 0

            club.diversity = diversity
            club.inclusivity = inclusivity
            club.time_commitment = time_commitment
            club.experience_requirement = experience_requirement
            club.workload = workload
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
    # clubs = get_all_clubs()
    # for club in clubs:
    #     print(club)

    #calculate_all_club_ratings()

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