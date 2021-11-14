from flask import Flask, request, make_response, jsonify
from flask import render_template, Response
from flask_sqlalchemy import SQLAlchemy
from casclient import CasClient
import os
DELETE_USER = 0
BLACKLIST_USER = 1
EDIT_USER = 2
EDIT_CLUB = 3
ADD_TAG = 4
app = Flask(__name__, template_folder=".")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://rvwhfgtoycqubz:e0cb0aca7c7da7773f28d1905455da0f9bf5e83d1a0b98be573e86a621c168e9@ec2-23-23-199-57.compute-1.amazonaws.com:5432/d8hudjmal9i0pc"
app.secret_key = os.urandom(16)
db = SQLAlchemy(app)

from db_search import *
from db_student_profile import *
from db_club_profile import *
from db_admin import *

def action_requests(request_type):
    if request_type == DELETE_USER:
        actions = ['/delete_user', '/review', '/reject']
    elif request_type == BLACKLIST_USER:
        actions = ['/blacklist_user', '/review', '/reject']
    elif request_type == EDIT_USER:
        actions = ['/edit_student', '/review', '/reject']
    elif request_type == EDIT_CLUB:
        actions = ['/edit_club', '/review', '/reject']
    elif request_type == ADD_TAG:
        actions = ['/add_tag', '/review', '.reject']

    return action_requests

@app.route("/", methods=["GET"])
@app.route("/login", methods=["GET"])
def login():
    try:
        html = render_template("login.html")
        response = make_response(html)
        response.delete_cookie('netid')
        return response
    except Exception:
        print("Whoops from login")

@app.route("/logout", methods=["GET"])
def logout():
    cas_client = CasClient()
    cas_client.authenticate()
    cas_client.logout('login')

@app.route("/admin", methods=["GET"])
def adminlogin():
    try:
        html = render_template("adminlogin.html")
        response = make_response(html)
        response.delete_cookie('netid')
        return response
    except Exception:
        print("uh oh admin login issue")

@app.route("/adminportal", methods=["GET"])
def adminportal():

    netid = request.cookies.get('netid')

    if netid is None:
        netid = request.args.get("netid")
    
    student = get_student_info(netid)
    adminStatus = student.admin
    name = student.name
    print('admin, ', adminStatus)

    try:
        if(not adminStatus):
            html = render_template("notadmin.html", netid = netid)
            response = make_response(html)
        else:
            html = render_template("adminportal.html", netid = netid, name=name)
            response = make_response(html)
        return response
    except:
        print("uh oh admin login validation issue")

@app.route("/landingwhoareyou", methods=["GET"])
def landingwhoareyou():
    auth_user = CasClient().authenticate()[:-1]

    user = get_student_info(auth_user)

    if (user.admin):
        html = render_template("studentoradmin.html")
        response = make_response(html)
        return response
    else:
        return landing()



@app.route("/landing", methods=["GET"])
def landing():
    # removes new line char (this was some weird ass formatting bug???)
    auth_user = CasClient().authenticate()[:-1]
    netid = request.cookies.get('netid')

    if netid is None:
        netid = auth_user
    
    clubname = request.args.get("clubname")
    studentname = request.args.get("studentname")

    if not clubname:
        clubname = ""
    if not studentname:
        studentname = ""
    
    print(clubname)
    print(studentname)

    user = get_student_info(netid)
    name = user.name
    clubs = club_search(clubname)
    students_list = student_search(studentname)

    print(clubs)
    print(students_list)
    if not clubs and not students_list:
        html = render_template("landing.html", netid=netid, name = name, hasClubs= False, hasStudents = False)
        print("if not clubs and not students_list:")
    elif not clubs:
        html = render_template("landing.html", netid=netid, name = name, hasClubs= False, hasStudents = True,students = students_list)
        print("elif not clubs:")
    elif not students_list:
        html = render_template("landing.html", netid=netid, name = name, clubs = clubs, studentname=studentname, clubname = clubname, hasClubs= True, hasStudents = False)
        print("elif not students_list:")
    else:
        html = render_template("landing.html", netid=netid, name = name, hasClubs = True, hasStudents = True, clubs = clubs, clubname = clubname, studentname=studentname, students = students_list)
        print("else")
        print(clubname)
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

@app.route("/studentsearch", methods=["GET"])
def studentsearch():

    netid = request.cookies.get('netid')
    print("HERE IS THE NETID RIGHT HERE", netid)
    studentname = request.args.get("studentname") 

    #print(netid)
    print(studentname)

    try:
        student = get_student_info(netid)
        if not student:
            html = render_template("studentsearch.html", netid = netid, hasStudents = False)
            print("hmm")
        else:
            name = student.name
            clubs = student.clubs
            html = render_template("studentsearch.html", netid = netid, hasStudents = True, name= name, clubs = clubs)
            students_list = student_search(studentname)
            print(students_list)
            clubs = club_search("")
            
            for student in students_list:
                print(student.name)

        return response
    except Exception:
        print("whoops from landing")
        print("whoops from student search")

#@app.route("/profileexternal", methods=["GET"])
#def profileexternal():
#    desirednetid = request.args.get("desirednetid")

# rendering profile page from landing page
@app.route("/profile", methods=["GET"])
def profile():
   
    try:
        diffperson = request.args.get("diffperson")
        # print(diffperson, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        netid = request.cookies.get("netid")
        
        if diffperson:
            student = get_student_info(diffperson)
        else:
            student = get_student_info(netid)
            diffperson = netid

        print(netid, "AAAAAAAAAAAAAAAAAAAAAA")

        name = student.name
        classyear = student.year
        major = student.major
        clubs = student.clubs
        bio = student.bio
        interests = student.tags

        html = render_template("profile.html", student = student, netid=netid, name=name,
        classyear=classyear, major=major, clubs=clubs,
        bio=bio, interests=interests, diffperson = diffperson)

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
    clubs = get_all_clubs()
    tags = get_all_tags()
    try:
        html = render_template("editprofile.html", netid=netid, clubs = clubs, tags = tags)
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

        print("better get to here")

        reviews = get_club_ratings(club.clubid)
        if not reviews:
            html = render_template("clubpage.html", netid = netid, clubname = club.name,
                                description = club.description, members = club.members,
                                tags = club.tags, 
                                hasScores = False)
        
        else:

            diversity = 0.0
            inclusivity = 0.0
            time_commitment = 0.0
            workload = 0.0
            experience_requirement = 0.0

            counter = 0
            for review in reviews:
                diversity += review.diversity
                print("??????????")
                inclusivity += review.inclusivity
                print("???zzzzz???????")
                time_commitment += review.time_commitment
                print("????aaa??????")
                workload += review.workload
                print("????56456??????")
                experience_requirement += review.experience_requirement
                print("????MMMM??????")

                counter += 1

            diversity /= counter
            inclusivity /= counter
            time_commitment /= counter
            workload /= counter
            experience_requirement /= counter

            print("MAMAMAAMMAMA")

            html = render_template("clubpage.html", netid = netid, clubname = club.name,
                                    description = club.description, members = club.members,
                                    tags = club.tags, 
                                    hasScores = True,
                                    diversity = diversity,
                                    inclusivity = inclusivity,
                                    time_commitment = time_commitment,
                                    workload = workload,
                                    experience_requirement = experience_requirement)
        response = make_response(html)
        return response
    except Exception:
        print("whoops from clubpage")

@app.route("/myratings", methods = ["POST", "GET"])
def myratings():
    try:
        netid = request.cookies.get("netid")
        student = get_student_info(netid=netid)
        name = student.name
        clubs = student.clubs
        print("this is hte netididddd", netid)
        ratings = get_student_ratings(netid)
        html = render_template("ratings_from_student.html", name = name, review = ratings, clubs = clubs)
        response = make_response(html)
        return response
    except Exception:
        print("whoops from ratings")

@app.route("/ranking", methods = ["POST","GET"])
def ranking():
    html = render_template("voting.html")
    response = make_response(html)
    return response

@app.route("/addrating", methods = ["POST","GET"])
def addrating():

    print("hahahahah we r here")

@app.route("/voting", methods = ["POST","GET"])
def vote():
    try:
        netid = request.cookies.get("netid")
        print("netid retrieved: ", netid)
        if request.method == 'POST':
            print("did we get here")
            clubname = request.form['clubname']
            diversity = request.form['diversity']
            inclusivity = request.form['inclusivity']
            workload = request.form['workload']
            time_commitment = request.form['time_commitment']
            experience_requirement = request.form['experience_requirement']
            add_rating(netid, clubname, diversity, inclusivity, time_commitment, experience_requirement, workload)
            msg = 'success'
        else:
            msg = 'huh we aren\'t supposed to be here'
        return jsonify(msg)
    except Exception:
        print("whoops from voting :(")

@app.route("/adminlanding", methods = ["GET"])
def adminlanding():
    auth_user = CasClient().authenticate()[:-1]
    user = get_student_info(auth_user)
    if (not user.admin):
        html = render_template("notadmin.html")
        response = make_response(html)
        return response

    html = render_template("adminlanding.html", requests = get_all_requests(), hasRequests = True)
    response = make_response(html)
    return response
    # try:
    #     auth_user = CasClient().authenticate()[:-1]
    #     user = get_student_info(auth_user)
    #     if (not user.admin):
    #         html = render_template("notadmin.html")
    #         response = make_response(html)
    #         return response

    #     html = render_template("adminlanding.html", requests = get_all_requests(), hasRequests = True)
    #     response = make_response(html)
    #     return response
    # except Exception:
    #     print("whoops from adminlanding")

@app.route("/delete_user")
def delete_user():
    netid = request.args.get("netid")
    clubname = request.args.get("clubname")
    delete_student_club(netid, clubname)

@app.route("/blacklist_user")
def blacklist_user():
    netid = request.args.get("netid")
    blacklist_student(netid)
    request_id = request.args.get("requestid")
    delete_request(request_id)

@app.route("/edit_student")
@app.route("/edit_club")

@app.route("/add_tag")
def add_tag():
    tagname = request.args.get("tagname")
    add_tag(tagname)
    request_id = request.args.get("requestid")
    delete_request(request_id)

@app.route("/reject")
def reject_request():
    request_id = request.args.get("requestid")
    delete_request(request_id)

@app.route("/adminclubs", methods=["GET"])
def adminclubs():
    auth_user = CasClient().authenticate()[:-1]
    user = get_student_info(auth_user)

    clubname = request.args.get("clubname")

    if not clubname:
        clubname = ""

    clubs = club_search(clubname)

    if (not user.admin):
        html = render_template("notadmin.html")
        response = make_response(html)
        return response

    html = render_template("adminclubs.html", hasClubs = 1, clubs=clubs)
    response = make_response(html)
    return response
