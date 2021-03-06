from app import db
from models import Student, Club, Tag, Review, Request

from db_admin import *
DELETE_USER = 0
BLACKLIST_USER = 1
EDIT_USER = 2
EDIT_CLUB = 3
ADD_TAG = 4
# def club_search(search):
#     clubs = None
#     search_query = '%' + search + '%'
#     clubs = Club.query.filter((Club.name.ilike(search_query) | Club.tags.any(Tag.name.ilike(search_query)))).all()
#     for club in clubs:
#         print(club)

def filter_by_tags(tags):
    clubs = Club.query.filter(Club.tags.any(Tag.name.in_(tags))).all()
    return clubs

def get_all_students():
    students = Student.query.paginate(page = 1, per_page = 20)
    return students

def get_all_reviews():
    reviews = Review.query.all()
    return reviews

def get_all_requests():
    requests = Request.query.all()
    return requests

def member_in_club(netid, clubid):
    student = Student.query.filter_by(netid = netid).first()
    club = Club.query.filter_by(name = clubid).first()
    members = club.members
    return student in members
    
# def get_all_tags():
#     tags = Tag.query.all()
#     return tags

# def update_club_info(name, description = None, members = None, tags = None):
#     club = Club.query.filter_by(name = name).first()

#     if description != "" and not None:
#         club.description = description
    
#     if members != "" and members is not None:
#         members = members.split(',')
#         for member in members:
#             member = member.strip()

#             student = Student.query.filter_by(name=member).first()
#             club.members.append(student)
#             db.session.add(club)

#     if tags != "" and tags is not None:
#         #tags = tags.split(',')
#         for tag in tags:
#             tag = tag.strip()
#             tag = Tag.query.filter_by(name=tag).first()
#             club.tags.append(tag)
#             db.session.add(club)

#     db.session.commit()

#     def calculate_all_club_ratings():
#         clubs = get_all_clubs()
#         for club in clubs:
#             reviews = get_club_ratings(club.clubid)
#             print(reviews)

#             diversity = 0.0
#             inclusivity = 0.0
#             time_commitment = 0.0
#             workload = 0.0
#             experience_requirement = 0.0
#             counter = 0

#             for review in reviews:
#                 diversity += review.diversity
#                 inclusivity += review.inclusivity
#                 time_commitment += review.time_commitment
#                 workload += review.workload
#                 experience_requirement += review.experience_requirement
#                 counter += 1
            
#             if diversity != 0:
#                 diversity /= counter
#                 inclusivity /= counter
#                 time_commitment /= counter
#                 workload /= counter
#                 experience_requirement /= counter
#             else:
#                 diversity = inclusivity = time_commitment = workload =experience_requirement = 0

#             club.diversity = diversity
#             club.inclusivity = inclusivity
#             club.time_commitment = time_commitment
#             club.experience_requirement = experience_requirement
#             club.workload = workload
#             db.session.commit()

# def add_request(request_type, netid_sender, netid_about = None, club = None, tagname = None):
#     if request_type == "delete_user":
#         request_type = DELETE_USER
#         club = Club.query.filter_by(name = club).first()
#         club = club.clubid
#     elif request_type == "blacklist_user":
#         request_type = BLACKLIST_USER  
#     elif request_type == "edit_user":
#         request_type = EDIT_USER
#     if request_type == "edit_club":
#         club = Club.query.filter_by(name = club).first()
#         club = club.clubid
#         request_type = EDIT_CLUB
#     elif request_type == "add_tag":
#         request_type = ADD_TAG
#     request = Request(request_type, netid_sender, netid_about, club, tagname)
#     db.session.add(request)
#     db.session.commit()

# def add_student_club(netid, clubname):
#     student = get_student_info(netid)
#     club = Club.query.filter_by(name = clubname).first()
#     club.members.append(student)
#     student.clubs.append(club)
#     db.session.add(student)
#     db.session.commit()

# # get list of all Club objects in club_info table
# def get_all_clubs(bool = False):
#     clubs = Club.query.all()
#     if bool:
#         clubs = Club.query.order_by(Club.inclusivity).all()
#     return clubs

def get_unrated_clubs(netid):
    student = Student.query.filter_by(netid = netid).first()
    clubs = student.clubs
    reviews = student.reviews
    rated = []
    unrated = []
    for review in reviews:
        club = review.club
        rated.append(club[0])
    for club in clubs:
        if club not in rated:
            unrated.append(club)
    return unrated

def calculate_club_rankings():
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
        

if __name__ == "__main__":
    calculate_club_rankings()
    clubs = Club.query.all()
    for club in clubs:
        print(club)
        print(club.ranking_over)
        print(club.ranking_div)
        print(club.ranking_inc)
        print(club.ranking_time)
        print(club.ranking_work)
        print(club.ranking_exp)
    # reviews = get_all_reviews()
    # # for review in reviews:
    # #     club = review.club
    # #     student = review.student
    # #     if not club or not student:
    # #         db.session.delete(review)
    # # db.session.commit()

    # requests = get_all_requests()
    # print(requests)
    # for request in requests:
    #     clubid = request.clubid
    #     club = Club.query.filter_by(clubid = clubid)
    #     if not club:
    #         db.session.delete(request)
    # db.session.commit()
    

    # club = Club.query.filter_by(name = "Aikido Club").first()
    # student = Student.query.filter_by(netid = "eagarwal").first()
    # (get_unrated_clubs(student.netid))
    # print(member_in_club('eagarwal', 'Mock Trial'))
    # print(member_in_club('ajguerra', 'Mock Trial'))
    # print(club)
    # print(club.reviews)
    # for review in club.reviews:
    #     reviewThis = Review.query.filter_by(reviewid = review.reviewid).first()
    #     print(reviewThis)

    # def update_club_info(name, description = None, members = None, tags = None):
    #     club = Club.query.filter_by(name = name).first()

    #     if description != "" and not None:
    #         club.description = description
        
    #     if members != "" and members is not None:
    #         members = members[1:-1]
    #         members = members.split(',')
    #         for member in members:
    #             member = member.strip()
    #             student = Student.query.filter_by(netid=member).first()
    #             print(student)
    #             club.members.append(student)
    #             db.session.add(club)

    #     if tags != "" and tags is not None:
    #         tags = tags[1:-1]
    #         tags = tags.split(',')
    #         for tag in tags:
    #             tag = tag.strip()
    #             tag = Tag.query.filter_by(name=tag).first()
    #             print(tag)
    #             club.tags.append(tag)
    #             db.session.add(club)

    #     db.session.commit()

    # update_club_info("TWN", 'the womens network!!!!', '[ajguerra, camilanv, nadiar]', '[Baseball, Basketball]')
    # # delete_student_club('camilanv', 1)
    # # delete_student_club('camilanv', 21)
    # # delete_student_club('camilanv', 20)
    # # delete_student_club('camilanv', 13)
    # # delete_student_club('camilanv', 20)
    # # delete_student_club('camilanv', 21)
    # # delete_student_club('camilanv', 1)
    # #print(get_all_requests())
    # # add_request(request_type="delete_user", netid_sender="eagarwal", netid_about="ajguerra", club = "SWE")
    # # add_request(request_type="edit_user", netid_sender="eagarwal", netid_about="ajguerra")
    # # add_request(request_type="edit_club", netid_sender="ajguerra", club = "PWICS")
    # # add_request(request_type="blacklist_user", netid_sender="ajguerra", netid_about="eagarwal")
    # # add_request(request_type="add_tag", netid_sender="ajguerra", tagname="Plants")
    # #add_review("eagarwal", "Roaring 20", 5, 4, 3, 4, 5)
    # # delete_review("eagarwal", "Roaring 20", 21)
    # # update_club_info("Roaring 20", tags = ("Dogs", "Coding", "SQL", "MCU", "Bowling", "Innovation"))
    # # update_club_info("Nassoons", tags = ("Dogs", "Coding", "SQL", "MCU", "Bowling", "Innovation"))
    # # update_club_info("eXpressions", tags = ("Dogs", "Coding", "SQL", "MCU", "Bowling", "Innovation"))
    # # update_club_info("SWE", tags = ("Dogs", "Coding", "SQL", "MCU", "Bowling", "Innovation"))
    # # update_club_info("PWICS", tags = ("Dogs", "Coding", "SQL", "MCU", "Bowling", "Innovation"))

    # # clubs = filter_by_tags(["Dogs", "League of Legends", "Coding"])
    # # print(clubs)
    # # clubs = get_all_clubs()
    # # for club in clubs:
    # #     print(club)

    # #calculate_all_club_ratings()

    # # add_tag('Beachball')
    # # add_tag('Sports')
    # # add_tag('Bowling')
    # # add_tag('Cricket')

    # # student = Student.query.filter_by(netid = 'eagarwal').first()
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