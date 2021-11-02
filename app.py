from flask import Flask, request, make_response
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, template_folder=".")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://rvwhfgtoycqubz:e0cb0aca7c7da7773f28d1905455da0f9bf5e83d1a0b98be573e86a621c168e9@ec2-23-23-199-57.compute-1.amazonaws.com:5432/d8hudjmal9i0pc"
db = SQLAlchemy(app)

from db1 import get_student_info, update_student_info, get_club_info, update_club_info, club_search, student_search, get_student_ratings

@app.route("/", methods=["GET"])
@app.route("/login", methods=["GET"])
def login():
    try:
        html = render_template("login.html")
        response = make_response(html)
        return response
    except Exception:
        print("Whoops from login")

@app.route("/landing", methods=["GET"])
def landing():

    netid = request.cookies.get('netid')

    if netid is None:
        netid = request.args.get("netid")
    
    clubname = request.args.get("clubname")

    if clubname is None:
        clubname = ""
    student = get_student_info(netid)
    name = student.name
    clubs = club_search(clubname)
    html = render_template("landing.html", netid=netid, name = name, clubs = clubs, clubname = clubname)
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response
 

@app.route("/studentsearch", methods=["GET"])
def studentsearch():

    netid = request.cookies.get('netid')
    studentname = request.args.get("studentname") 

    #print(netid)
    print(studentname)

    try:
        students_list = student_search(studentname)
        print(students_list)
        print("did i make it here")
        
        for student in students_list:
            print(student.name)

        print("how about here")
        html = render_template("studentsearch.html", students = students_list)
        print("okay well did i make it here")
        response = make_response(html)
        # print("before")
        # response.set_cookie('studentname', studentname)
        # print("after")
        return response
    except Exception:
        print("whoops from student search")

@app.route("/profileexternal", methods=["GET"])
def profileexternal():
    desirednetid = request.args.get("desirednetid")
    

# rendering profile page from landing page
@app.route("/profile", methods=["GET"])
def profile():
   
    try:
        netid = request.args.get("netid")
        student = get_student_info(netid)
        name = student.name
        classyear = student.year
        major = student.major
        clubs = student.clubs
        bio = student.bio
        interests = student.tags

        html = render_template("profile.html", student = student, netid=netid, name=name,
        classyear=classyear, major=major, clubs=clubs,
        bio=bio, interests=interests)

        response = make_response(html)
        return response
    except Exception:
        print("whoops from profile")

# rendering profile page after updating from editprofile.html
@app.route("/profilefromedit", methods=["GET"])
def edited_profile():

    try:
        netid = request.args.get("netid")
        bio = request.args.get("bio")
        clubs = request.args.get("clubs")
        tags = request.args.get("tags")
        update_student_info(netid, bio, clubs, tags)
        return profile()
    except Exception:
        print("whoops profile from edit")

# rendering edit profile page from the profile page
@app.route("/editprofile", methods=["GET"])
def editprofile():
    netid = request.args.get("netid")
    try:
        html = render_template("editprofile.html", netid=netid)
        response = make_response(html)
        return response
    except Exception:
        print("whoops from editprofile")

@app.route("/clubpage", methods=["GET"])
def clubpage():
    try:
        clubname = request.args.get("clubname")
        netid = request.args.get("netid")
        club = get_club_info(clubname)
        html = render_template("clubpage.html", netid = netid, clubname = club.name,
                                description = club.description, members = club.members,
                                tags = club.tags)
        response = make_response(html)
        return response
    except Exception:
        print("whoops from clubpage")

@app.route("/myratings", methods = ["GET"])
def myratings():
    try:
        netid = request.args.get("netid")
        student = get_student_info(netid)
        name = student.name
        ratings = get_student_ratings(netid)
        html = render_template("myratings.html", netid = netid, name = name, ratings = ratings)
        response = make_response(html)
        return response
    except Exception:
        print("whoops from ratings")