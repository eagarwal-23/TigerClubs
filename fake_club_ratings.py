from app import db
from models import Club, Student, Tag
import pandas as pd
import random

def get_all_clubs():
    clubs = Club.query.all()
    return clubs

def get_all_clubnames():
    clubs = Club.query.order_by(Club.name).all()
    final = list()
    for club in clubs:
        final.append(club.name)
    return final

def get_all_netids():
    students = Student.query.order_by(Student.name).all()
    final = list()
    for student in students:
        final.append(student.netid)
    return final

def get_all_students():
    students = Student.query.all()
    return students

def add_students_club(students, clubname):
    club = Club.query.filter_by(name = 'Armenian Club').first()
    print(club)
    for student in students:
        student = Student.query.filter_by(netid=student).first()
        club.members.append(student)
        db.session.add(club)
    print(club.members)

STUDENTS = ['eagarwal', 'jg41', 'nreptak', 'camilanv',
            'nadiar', 'ajguerra']

if __name__ == "__main__":
    # n_students = 50
    # n_members = 10
    # students = get_all_netids()
    # selected_students = (random.sample(students, n_students))
    # #print(selected_students)
    # students = selected_students + STUDENTS

    # # list of 100 random students + 5 of us
    # eesha = Student.query.filter_by(netid='eagarwal').first()
    # camila = Student.query.filter_by(netid='camilanv').first()
    # natalie = Student.query.filter_by(netid='nreptak').first()
    # nadia = Student.query.filter_by(netid='nadiar').first()
    # anthony = Student.query.filter_by(netid='ajguerra').first()
    # josh = Student.query.filter_by(netid='jg41').first()

    # students.append(eesha)
    # students.append(camila)
    # students.append(nadia)
    # students.append(natalie)
    # students.append(anthony)
    # students.append(josh)

    # members = random.sample(students, n_members)
    # #print(members)
    # clubs = get_all_clubnames()
    # club = clubs[0]
    # add_students_club(members, club)

    # clubs = get_all_clubs()
    # club = clubs[0]
    #print(club.members)
    # for club in clubs:
    #     print(club, club.members)

    # list of all clubs
    #print(students)
    # for club in clubs:
    #     print(club.members)
        # members = random.sample(students, n_members)
        # add_students_club(members, club.name)

    clubs = get_all_clubs()
    for club in clubs:
        tag = Tag.query.filter_by(name = 'Baseball').first()
        club.tags.append(tag)
        diversity = random.randrange(1, 5)
        inclusivity = random.randrange(1, 5)
        time_commitment = random.randrange(1, 5)
        experience_requirement = random.randrange(1, 5)
        workload = random.randrange(1, 5)
        club.diversity = diversity
        club.inclusivity = inclusivity
        club.time_commitment = time_commitment
        club.experience_requirement = experience_requirement
        club.workload = workload 
        db.session.add(club)
        db.session.commit()