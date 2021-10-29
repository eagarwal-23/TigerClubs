from flask import Flask, request, make_response
from flask import render_template
from student_db import get_student_info, update_student_info

app = Flask(__name__, template_folder=".")

@app.route("/", methods=["GET"])
@app.route("/login", methods=["GET"])
def login():
    try:
        html = render_template("login.html")
        response = make_response(html)
        return response
    except Exception:
        print("Whoops")


@app.route("/landing", methods=["GET"])
def landing():
    netid = request.args.get("netid")

    try:
        html = render_template("landing.html", netid=netid)
        response = make_response(html)
        return response
    except Exception:
        print("whoops")


@app.route("/profile", methods=["GET"])
def profile():
    netid = request.args.get("netid")
    # student_info = get_student_info(netid)
    html = render_template("profile.html", netid=netid)

    # html = render_template("profile.html",
    # name= student_info.get_name(),
    # netid= student_info.get_netid(),
    # classyear= student_info.get_year(),
    # major= student_info.get_major(),
    # clubs= student_info.get_clubs(),
    # bio=student_info.get_bio,
    # interests=student_info.get_interests())

    response = make_response(html)
    return response

@app.route("/editprofile", methods=["GET"])
def editprofile():
    netid = request.args.get("netid")
    # profile_information = get_profile_information(netid)
    html = render_template("editprofile.html", netid=netid)
    #html = render_template("profile.html",
    #name=name,
    #netid=netid,
    #classyear=classyear,
    #major=major,
    #clubs=clubs,
    #bio=bio,
    #interests=interests)
    response = make_response(html)
    return response
    