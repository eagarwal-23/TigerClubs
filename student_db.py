#!/usr/bin/env python

#-----------------------------------------------------------------------
#   club.py
#   Authors: Eesha Agarwal and
#   Module for functions related to student's own profile page

from sys import argv, stderr, exit
from psycopg2 import connect, sql
from contextlib import closing
from student import Student

# add database details as constants
DB = 'd8hudjmal9i0pc'
USERNAME = 'rvwhfgtoycqubz'
PASSWORD = 'e0cb0aca7c7da7773f28d1905455da0f9bf5e83d1a0b98be573e86a621c168e9'
HOST = 'ec2-23-23-199-57.compute-1.amazonaws.com'
PORT = '5432'
DB_URL = 'postgres://rvwhfgtoycqubz:e0cb0aca7c7da7773f28d1905455da0f9bf5e83d1a0b98be573e86a621c168e9@ec2-23-23-199-57.compute-1.amazonaws.com:5432/d8hudjmal9i0pc'

# given netid and password, return corresponding student info from database
# for student profile page
def get_student_info(netid):
    try:
        with connect(DB_URL, sslmode = 'require') as connection:
            with closing(connection.cursor()) as cursor:
                
                # get student name, netid, year, major, bio
                
                cursor = cursor.execute(get_student_info_query(), [netid])
                student_info = cursor.fetchone()

                # get students clubs
                clubs = []
                cursor = cursor.execute(get_student_clubs_query(), [netid])
                row = cursor.fetchone()

                while row is not None:
                    club = club[0]
                    if club not in clubs:
                        clubs.append(club)
                    row = cursor.fetchone()

                # get students tags (interests)
                tags = []
                cursor = cursor.execute(get_student_tags_query(), [netid])
                row = cursor.fetchone()

                while row is not None:
                    tag = tag[0]
                    if tag not in tags:
                        tags.append(tag)
                    row = cursor.fetchone()

                student_profile = Student(student_info[0], student_info[1],
                                        student_info[2], student_info[3],
                                        student_info[4], clubs, tags, student_info[5])

                return student_profile

    except Exception as ex:
        print(ex, file = stderr)
        exit(1)

def update_student_info(netid, bio = None, clubs = None, tags = None):
    try:
        with connect(database=DB, user=USERNAME, password=PASSWORD, host=HOST, port= PORT) as connection:
            with closing(connection.cursor()) as cursor:

                clubid = clubs

                # update student's bio
                if bio:
                    cursor = cursor.execute(update_student_bio_query(), [bio, netid])
                if clubs:
                    cursor = cursor.execute(edit_student_clubs(), [netid, clubs])
                if tags:
                    cursor = cursor.execute(edit_student_tags(), [netid, tags])

                connection.commit()

    except Exception as ex:
        print(ex, file = stderr)
        exit(1)

# query to update student's bio in student_info table
def update_student_bio_query():
    stmt_str = "UPDATE student_info "
    stmt_str += "SET bio = %s "
    stmt_str += "WHERE netid = %s"

    return stmt_str

# query to edit student's clubs
def edit_student_clubs():
    stmt_str = "INSERT INTO student_clubs(netid, clubid) "
    stmt_str = "VALUES (%s, %s)"

    return stmt_str

# query to edit student's tags
def edit_student_tags():
    stmt_str = "INSERT INTO student_tags(netid, tagid) "
    stmt_str = "VALUES (%s, %s)"
    #
    return stmt_str

# query to get student ingo
def get_student_info_query():
    stmt_str = "SELECT netid, name, res_college, year, major, bio "
    stmt_str += "FROM student_info "
    stmt_str += "WHERE netid = %s"

    return stmt_str

# query to get student's clubs
def get_student_clubs_query():
    stmt_str = "SELECT club_info.name, clubid "
    stmt_str += "FROM club_info, students_clubs "
    stmt_str += "WHERE students_clubs.clubid = club_info.clubid "
    stmt_str += "AND student_clubs.netid = %s "
    stmt_str += "ORDER BY club_info.name"

    return stmt_str


# query to get student's tags
def get_student_tags_query():
    stmt_str = "SELECT tag_info.name, tagid "
    stmt_str += "FROM tag_info, students_tags "
    stmt_str += "WHERE students_tags.tagid = tag_info.tagid "
    stmt_str += "AND student_tags.netid = %s "
    stmt_str += "ORDER BY tag_info.name"

    return stmt_str