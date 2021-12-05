from app import db
from fake_club_ratings import add_students_club
from models import Club, Student, Tag, Review
import pandas as pd
import random

EXISTING_CLUBS = [1, 2, 5, 6, 8, 10, 11, 12, 13, 15, 16, 27]
NUM_MEMBERS = 25

def get_all_students():
    students = Student.query.all()
    return students

def get_all_clubs():
    clubs = Club.query.all()
    return clubs

def add_club(name, description, club_type, diversity = 0, 
    inclusivity = 0, time_commitment = 0,
    experience_requirement = 0, workload = 0):
    club = Club(name, description, club_type, diversity, 
                inclusivity, time_commitment, experience_requirement, 
                workload)
    club.diversity = 0
    club.inclusivity = 0
    club.time_commitment = 0
    club.experience_requirement = 0
    club.workload = 0
    db.session.add(club)
    db.session.commit()

def tag_in_db(tagname):
    this_tag = Tag.query.filter_by(name = tagname).first()
    all_tags = Tag.query.all()
    return (this_tag in all_tags)

def club_in_db(clubname):
    this_club = Club.query.filter_by(name = clubname).first()
    all_clubs = Club.query.all()
    return (this_club in all_clubs)

def add_tag(tagname):
    tag = Tag(tagname)
    db.session.add(tag)
    db.session.commit()

def add_tags_club(tagnames, clubname):
    club = Club.query.filter_by(name = clubname).first()
    for tagname in tagnames:
        if tag_in_db(tagname):
            tag = Tag.query.filter_by(name = tagname).first()
        else:
            tag = Tag(name = tagname)
        club.tags.append(tag)
        db.session.add(club)
    db.session.commit()

def add_students_club(students, clubname):
    club = Club.query.filter_by(name = clubname).first()
    for student in students:
        club.members.append(student)
        db.session.add(club)
    db.session.commit()

def remove_all_members(clubname):
    club = Club.query.filter_by(name = clubname).first()
    new_members = []
    club.members = new_members
    db.session.add(club)
    db.session.commit()

def remove_all_tags(clubname):
    club = Club.query.filter_by(name = clubname).first()
    new_tags = []
    club.tags = new_tags
    db.session.add(club)
    db.session.commit()

def remove_all_reviews(clubname):
    club = Club.query.filter_by(name = clubname).first()
    reviews = club.reviews
    new_reviews = []
    club.reviews = new_reviews
    db.session.add(club)
    for review in reviews:
        reviewThis = Review.query.filter_by(reviewid = review.reviewid).first()
        db.session.delete(reviewThis)
    print(club.reviews)
    db.session.commit()

def delete_added_clubs():
    clubs = get_all_clubs()
    for club in clubs:
        clubid = club.clubid
        if not clubid in EXISTING_CLUBS:
            db.session.delete(club)
    db.session.commit()

# read in club data and add to db
# add 25 randomly selected students as
# members to each club
if __name__ == "__main__":
    filename = "club_data.xlsx"
    df = pd.read_excel(filename)
    print(df.head(5))
    students = get_all_students()
    for i in range(len(df)):
        clubname = df.loc[i, "name"]
        description = df.loc[i, "description"]
        club_type = df.loc[i, "type"]
        tags = (df.loc[i, "tags"]).split(",")
        if tags[0] == '-':
            tags = ['All']
        for i in range(len(tags)):
            tags[i] = tags[i].strip()

        if not club_in_db(clubname):
            add_club(clubname, description, club_type)
            if not tags == []:
                add_tags_club(tags, clubname)
        
        selected_students = (random.sample(students, NUM_MEMBERS))
        add_students_club(selected_students, clubname)

        # if not club_in_db(clubname):
        #     add_club(clubname, description, club_type)
        #     f

    # for i in range(len(df)):
    #     clubname = df.loc[i, "name"]
    #     clubdesc = df.loc[i, "description"]
    #     clubtype = df.loc[i, "type"]
    #     add_club(name = clubname,
    #             description = clubdesc,
    #             club_type= clubtype, diversity = 0, 
    #             inclusivity = 0, 
    #             time_commitment = 0, 
    #             experience_requirement = 0, 
    #             workload = 0)
