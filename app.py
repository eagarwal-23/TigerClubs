from flask import Flask, request, make_response
from flask import render_template
from student_db import get_student_info, update_student_info
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, template_folder=".")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://rvwhfgtoycqubz:e0cb0aca7c7da7773f28d1905455da0f9bf5e83d1a0b98be573e86a621c168e9@ec2-23-23-199-57.compute-1.amazonaws.com:5432/d8hudjmal9i0pc"
db = SQLAlchemy(app)

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

    netid = request.args.get("netid")
    try:
        student = get_student_info(netid)
        name = student.get_name()
        clubs = student.get_clubs()
        html = render_template("landing.html", netid=netid, name = name, clubs = clubs, student = student)
        response = make_response(html)
        return response
    except Exception:
        print("whoops from landing")

# rendering profile page from landing page
@app.route("/profile", methods=["GET"])
def profile():
    netid = request.args.get("netid")

    try:
        student = get_student_info(netid)
        name = student.get_name()
        classyear = student.get_year()
        major = student.get_major()
        clubs = student.get_clubs()
        bio = student.get_bio()
        interests = student.get_interests()

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
    netid = request.args.get("netid")
    bio = request.args.get("bio")
    clubs = request.args.get("clubs")
    tags = request.args.get("tags")

    try:

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
    clubname = request.args.get("clubname")
    try:
        #club = get_club_info(clubname) <--- db search for club info!
        html = render_template("clubpage.html", clubname=clubname)
        response = make_response(html)
        return response
    except Exception:
        print("whoops from clubpage")