from flask import Flask, request, make_response
from flask import render_template
from student_db import get_student_info, update_student_info
# from student import Student

app = Flask(__name__, template_folder=".")

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
        html = render_template("landing.html", netid=netid)
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

        html = render_template("profile.html", netid=netid, name=name,
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
    bio = request.arts.get("bio")
    clubs = request.args.get("clubs")
    tags = request.args.get("tags")

    try:

        update_student_info(netid, bio, clubs, tags)
        profile()
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