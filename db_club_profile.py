from app import db
from models import Student, Club, Tag, Review
from db_search import get_all_clubs

# get Club object given clubname
def get_club_info(clubname):
    club = Club.query.filter_by(name = clubname).first()
    return club

# edit Club's information given clubname
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

# get all ratings for a Club given clubid
def get_club_ratings(clubid):
    club = Club.query.filter_by(clubid = clubid).first()
    reviews = club.reviews
    return reviews

# for all clubs, recalculate aggregate ratings'
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
        
        diversity /= counter
        inclusivity /= counter
        time_commitment /= counter
        workload /= counter
        experience_requirement /= counter

        club.diversity = diversity
        club.inclusivity = inclusivity
        club.time_commitment = time_commitment
        club.experience_requirement = experience_requirement
        club.workload = workload