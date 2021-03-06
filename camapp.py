from re import S
from flask import Flask, request, make_response, jsonify
import datetime as dt
from flask import render_template, Response
from flask_sqlalchemy import SQLAlchemy
from casclient import CASClient
import os
DELETE_USER = 0
BLACKLIST_USER = 1
EDIT_USER = 2
EDIT_CLUB = 3
ADD_TAG = 4
app = Flask(__name__, template_folder=".")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://rvwhfgtoycqubz:e0cb0aca7c7da7773f28d1905455da0f9bf5e83d1a0b98be573e86a621c168e9@ec2-23-23-199-57.compute-1.amazonaws.com:5432/d8hudjmal9i0pc"
app.secret_key = b'!*&y\xc9h`*u\xe0%-\xf2\xbc1\xa8\xd0gF\xc0\x89Y\xb4\xbe'
db = SQLAlchemy(app)

from db_search import *
from db_student_profile import *
from db_club_profile import *
from db_admin import *

_cas = CASClient()

ratings_period = dt.date(2021, 12, 21)

@app.before_request
def enforceHttpsInHeroku():
    # always force redirect to HTTPS (secure connection)
    if request.headers.get("X-Forwarded-Proto") == "http":
        url = request.url.replace("http://", "https://", 1)
        code = 301
        return redirect(url, code=code)

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
        return response
    except Exception:
        print("Whoops from login")

@app.route("/logout", methods=["GET"])
def logout():
    _cas.logout('login')

@app.route("/admin", methods=["GET"])
def adminlogin():
    try:
        html = render_template("adminlogin.html")
        response = make_response(html)
        return response
    except Exception:
        print("uh oh admin login issue")

@app.route("/adminportal", methods=["GET"])
def adminportal():

    netid = _cas.authenticate()
    netid = netid.rstrip()
    
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
    auth_user = _cas.authenticate()

    user = get_student_info(auth_user)

    if (user.admin):
        html = render_template("studentoradmin.html")
        response = make_response(html)
        return response
    else:
        return landing()

@app.route("/landing", methods=["GET"])
def landing():

    # netid = _cas.authenticate()
    # netid = netid.rstrip()
    netid = "camilanv"

    filter_tags = request.args.getlist("tags")
    if not filter_tags:
        filter_tags = get_all_tagnames()
    sort_criteria = request.args.get('sort_club')
    if not sort_criteria:
        sort_criteria = 'combined'
    else:
        print(sort_criteria)
    
    clubname = request.args.get("clubname")
    studentname = request.args.get("studentname")
    pagenum = request.args.get('page', 1, type=int)


    if not clubname:
        clubname = ""
    if not studentname:
        studentname = ""
    
    print(clubname)
    print(studentname)

    user = get_student_info(netid)
    isAdmin = 0
    if user.admin:
        isAdmin = 1
    
    name = user.name
    clubs = club_search(search = clubname, query = sort_criteria, tags = filter_tags)
    students_list = student_search(studentname, pagenum = pagenum, per_page= 21)
    tags = get_all_tags()

    if not clubs:
        html = render_template("mylanding.html", netid=netid, name = name, hasClubs= False, tags = tags, sort_by = sort_criteria, isAdmin = isAdmin)
        print("if not clubs:")
    else:
        html = render_template("mylanding.html", netid=netid, name = name, hasClubs = True, clubs = clubs, clubname = clubname, tags = tags, sort_by = sort_criteria, isAdmin = isAdmin)
        print("else")
        print(clubname)
    
    response = make_response(html)
    return response

@app.route("/studentsearch", methods=["GET"])
def studentsearch():

    # netid = _cas.authenticate()
    # netid = netid.rstrip()
    netid = "camilanv"
    studentname = request.args.get("studentname")
    pagenum = request.args.get('page', 1, type=int)

    if not studentname:
        studentname = ""
    
    print(studentname)

    user = get_student_info(netid)
    isAdmin = 0
    if user.admin:
        isAdmin = 1

    name = user.name
    students_list = student_search(studentname, pagenum = pagenum, per_page= 21)

    print(students_list.items)
    
    if not students_list:
        html = render_template("student.html", netid=netid, name = name, studentname=studentname, hasClubs= True, hasStudents = False, isAdmin = isAdmin)
        print("elif not students_list:")
    else:
        html = render_template("student.html", netid=netid, name = name, hasClubs = True, hasStudents = True, studentname=studentname, students = students_list, isAdmin = isAdmin)
        print("else")
    response = make_response(html)
    return response

@app.route("/profile", methods=["GET"])
def profile(diffperson=None):
   
    try:
        print('we made it to profile')
        if diffperson is None:
            diffperson = request.args.get("diffperson")
        print("no diff person", diffperson)
        # netid = _cas.authenticate()
        # netid = netid.rstrip()
        netid = "camilanv"

        print("net id found?")
        if diffperson:
            student = get_student_info(diffperson)
        else:
            student = get_student_info(netid)
            diffperson = netid
        
        isAdmin = 0
        if student.admin:
            isAdmin = 1

        name = student.name
        classyear = student.year
        major = student.major
        clubs = student.clubs
        bio = student.bio
        interests = student.tags
        tags = get_all_tags()

        html = render_template("profile.html", student = student,  name=name, netid= netid,
        classyear=classyear, major=major, clubs=clubs, tags=tags,
        bio=bio, interests=interests, diffperson = diffperson, isAdmin = isAdmin)

        response = make_response(html)
        return response
    except Exception:
        print("whoops from profile")

# rendering profile page after updating from editprofile.html
@app.route("/profilefromedit", methods=["GET"])
def edited_profile():

    try:
        # netid = _cas.authenticate()
        # netid = netid.rstrip()
        netid = "camilanv"

        realnetid = request.args.get("netid")
        bio = request.args.get("bio")
        clubs = request.args.getlist("clubs")
        tags = request.args.getlist("tags")
        update_student_info(realnetid, bio, clubs, tags)
        return profile(diffperson=realnetid)
    except Exception:
        print("whoops profile from edit")

# rendering edit profile page from the profile page
@app.route("/editprofile", methods=["GET"])
def editprofile():
    # netid = _cas.authenticate()
    # netid = netid.rstrip()
    netid = "camilanv"
    
    student = get_student_info(netid)

    isAdmin = 0
    if student.admin:
        isAdmin = 1
    
    name = student.name
    classyear = student.year
    major = student.major
    bio = student.bio
    clubs = get_all_clubs()
    tags = get_all_tags()
    try:
        html = render_template("myeditpage.html", name=name, netid=netid, student = student, clubs = clubs, tags = tags,
        classyear=classyear, major=major,
        bio=bio, isAdmin = isAdmin)
        response = make_response(html)
        return response
    except Exception:
        print("whoops from editprofile")


@app.route("/clubpage", methods=["GET"])
def clubpage():
    try:
        # netid = _cas.authenticate()
        # netid = netid.rstrip()
        netid = "camilanv"
       
        student = get_student_info(netid)

        isAdmin = 0
        if student.admin:
            isAdmin = 1
        
        clubname = request.args.get("clubname")
        club = get_club_info(clubname)

        html = render_template("clubpage.html", clubname = club.name,
                                    description = club.description, members = club.members,
                                    tags = club.tags, 
                                    hasScores = True,
                                    diversity = "{:.1%}".format((club.diversity/5)),
                                    inclusivity = "{:.1%}".format((club.inclusivity/5)),
                                    time_commitment = "{:.1%}".format((club.time_commitment/5)),
                                    workload = "{:.1%}".format((club.workload/5)),
                                    experience_requirement = "{:.1%}".format((club.experience_requirement/5)),
                                    isAdmin = isAdmin)
        response = make_response(html)
        return response

    except Exception:
        print("whoops from clubpage")

@app.route("/myratings", methods = ["POST", "GET"])
def myratings():
    try:
        # netid = _cas.authenticate()
        # netid = netid.rstrip()
        netid = "camilanv"
        student = get_student_info(netid=netid)

        isAdmin = 0
        if student.admin:
            isAdmin = 1
        today = dt.date.today()
        #if today == ratings_period:
        if True:
            name = student.name
            clubs = student.clubs
            ratings = get_student_ratings(netid)
            html = render_template("myratings.html", name = name, review = ratings, clubs = clubs, isAdmin = isAdmin)
            response = make_response(html)
            return response
        else:
            html = render_template("notmyratings.html", ratings_period=ratings_period, today=today, isAdmin = isAdmin)
            response = make_response(html)
            return response
    except Exception as e:
        print(e, "whoops from ratings")

@app.route("/voting", methods = ["POST","GET"])
def vote():
    try:
        netid = _cas.authenticate()
        netid = netid.rstrip()
        if request.method == 'POST':
            clubname = request.form['clubname']
            diversity = request.form['diversity']
            inclusivity = request.form['inclusivity']
            workload = request.form['workload']
            time_commitment = request.form['time_commitment']
            experience_requirement = request.form['experience_requirement']
            text_review = request.form["text_review"]
            print(text_review)
            add_rating(netid, clubname, diversity, inclusivity, time_commitment, experience_requirement, workload, text_review)
            msg = 'success'
        else:
            msg = 'huh we aren\'t supposed to be here'
        return jsonify(msg)
    except Exception:
        print("whoops from voting :(")

@app.route("/removingvote", methods= ["POST", "GET"])
def removingvote():
    try:
        if request.method == 'POST':
            reviewid = request.form['reviewid']
            delete_rating(reviewid)
            msg = 'success'
        else:
            msg = "uh oh"
        return jsonify(msg)
    except Exception:
        print("whoops from student removing review")

@app.route("/adminlanding", methods = ["GET"])
def adminlanding():
    auth_user = _cas.authenticate()
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

@app.route("/delete_user", methods = ["POST","GET"])
def delete_user():
    netid = request.args.get("netid")
    clubid = request.args.get("clubid")
    delete_student_club(netid=netid.strip(), clubid=clubid.strip())
    requestid = request.args.get("requestid")
    delete_request(requestid)
    msg = 'success'
    return jsonify(msg)

@app.route("/blacklist_user")
def blacklist_user():
    netid = request.args.get("netid")
    blacklist_student(netid)
    requestid = request.args.get("requestid")
    delete_request(requestid)
    msg = 'success'
    return jsonify(msg)

@app.route("/edit_student")
@app.route("/edit_club")

@app.route("/add_tag", methods = ['GET', 'POST'])
def add_tag():
    tagname = request.args.get("tagname")
    add_tag_db(tagname)
    requestid = request.args.get("requestid")
    delete_request(requestid)
    msg = 'success'
    return jsonify(msg)

@app.route("/reject_request", methods = ['GET'])
def reject_request():
    request_id = request.args.get("requestid")
    delete_request(request_id)
    msg = 'success'
    return jsonify(msg)

@app.route("/adminclubs", methods=["GET"])
def adminclubs():
    auth_user = _cas.authenticate()
    user = get_student_info(auth_user)

    if (not user.admin):
        html = render_template("notadmin.html")
        response = make_response(html)
        return response

    clubname = request.args.get("clubname")

    if not clubname:
        clubname = ""

    clubs = club_search(clubname)

    html = render_template("adminclubs.html", clubs=clubs)
    response = make_response(html)
    return response

@app.route("/adminstudents", methods=["GET"])
def adminstudents():
    netid = _cas.authenticate()
    netid = netid.rstrip()
    user = get_student_info(netid)

    if (not user.admin):
        html = render_template("notadmin.html")
        response = make_response(html)
        return response

    studentname = request.args.get("studentname")
    pagenum = request.args.get('page', 1, type=int)

    if not studentname:
        studentname = ""

    name = user.name
    students_list = student_search(studentname, pagenum = pagenum, per_page= 20)

    
    if not students_list:
        html = render_template("adminstudents.html", netid=netid, name = name, studentname=studentname, hasClubs= True, hasStudents = False)
        print("elif not students_list:")
    else:
        html = render_template("adminstudents.html", netid=netid, name = name, hasClubs = True, hasStudents = True, studentname=studentname, students = students_list)
        print("else")
    response = make_response(html)
    return response

@app.route("/adminrequests", methods=["GET"])
def adminrequests():
    auth_user = _cas.authenticate()
    user = get_student_info(auth_user)
    if (not user.admin):
        html = render_template("notadmin.html")
        response = make_response(html)
        return response

    html = render_template("adminrequests.html", requests = get_all_requests(), hasRequests = True)
    response = make_response(html)
    return response

@app.route("/adminclubpage", methods=["GET"])
def adminclubpage():
    try:
        netid = _cas.authenticate()
        netid = netid.rstrip()
       
        student = get_student_info(netid)

        isAdmin = 0
        if student.admin:
            isAdmin = 1
        
        clubname = request.args.get("clubname")
        club = get_club_info(clubname)

        html = render_template("admin-clubpage.html", clubname = club.name,
                                    description = club.description, members = club.members,
                                    tags = club.tags, 
                                    hasScores = True,
                                    diversity = "{:.1%}".format((club.diversity/5)),
                                    inclusivity = "{:.1%}".format((club.inclusivity/5)),
                                    time_commitment = "{:.1%}".format((club.time_commitment/5)),
                                    workload = "{:.1%}".format((club.workload/5)),
                                    experience_requirement = "{:.1%}".format((club.experience_requirement/5)),
                                    isAdmin = isAdmin)
        response = make_response(html)
        return response

    except Exception:
        print("whoops from clubpage")

@app.route("/editclub", methods=["GET"])
def editclub():
    auth_user = _cas.authenticate()
    user = get_student_info(auth_user)

    if (not user.admin):
        html = render_template("notadmin.html")
        response = make_response(html)
        return response

    clubname = request.args.get("clubname")
    if clubname is None:
        clubname = ""
    
    print("clubname:", clubname)
    club = get_club_info(clubname)

    html = render_template("editclubs.html",
                            name = club.name,
                            description = club.description,
                            members = club.members,
                            tags = club.tags)
    response = make_response(html)
    return response

@app.route("/editclubfromedit", methods=["GET"])
def editclubfromedit():
#try: bob
    name = request.args.get("name")
    description = request.args.get("description")
    members = request.args.get("members")
    tags = request.args.get("tags")

    print("am i whooping here before?????", name, description, members, tags)

    update_club_info(name, description, members, tags)
    print("whooping hereeeeee???")
    return adminclubs()
#except Exception:
    print("whoops from editclubfromedit")

@app.route("/delete_club", methods = ["GET"])
def delete_club():
   clubid = request.args.get("clubid")
   delete_club_db(clubid)
   msg = 'success'
   return jsonify(msg)

@app.route("/admintags", methods=["GET"])
def admintags():
    auth_user = _cas.authenticate()
    user = get_student_info(auth_user)
    if (not user.admin):
        html = render_template("notadmin.html")
        response = make_response(html)
        return response

    tagsearch = request.args.get("tag")
    if tagsearch is None:
        tagsearch = ""
    
    tags = tag_search(tagsearch)

    html = render_template("admintags.html", tags=tags)
    response = make_response(html)
    return response

@app.route("/updatingtags", methods=["POST","GET"])
def updatingtags():
    print("IVE GOTT")
    newtagname = request.form["newtagname"]
    id = request.form["tagid"]
    print("THE ID AND THE NAMEEEE", newtagname, id)
    edit_tag_db(id, newtagname)
    msg = "Editted!"
    return jsonify(msg)

@app.route("/deletetag", methods=["GET"])
def deletetag():
    tagid = request.args.get("tagid")
    print("WHAT IS THE TAG??", tagid)
    delete_tag_db_id(tagid)
    msg = "Deleted!"
    return jsonify(msg)

@app.route("/sort_clubs", methods = ["GET"])
def sort_clubs():
    sort_criteria = request.args.get('sort_club')
    clubs = club_search("", query = sort_criteria)
    print(clubs)

@app.route("/report", methods = ["GET"])
def file_report():
    netid = _cas.authenticate()
    netid = netid.rstrip()
    clubs = get_all_clubs()
    students = get_all_students()
    html = render_template("requestform.html", clubs = clubs, students = students)
    response = make_response(html)
    return response

@app.route("/submittedrequest", methods = ["GET"])
def submitted_request():
    netid = _cas.authenticate()
    netid = netid.rstrip()

    # student = get_student_info(netid)
    # isAdmin = 0
    #if student.admin:
    #    isAdmin = 1

    print(request.args)
    request_reason = request.args.get("reason")
    about_user = request.args.get("reportedUser")
    club = request.args.get("clubname")
    tag = request.args.get("tag")
    descrip = request.args.get("explanation")
    print(about_user)
    print(request_reason)
    success = add_request(request_reason, netid, about_user, club, tag, descrip)
    if success == None:
        html = render_template("wrongrequestinput.html")
    else:
        html = render_template("requestsubmitted.html")
    response = make_response(html)
    return response

@app.route("/creatingtags", methods=["POST"])
def creatingtags():
    newtag = request.form["newtag"]
    add_tag_db(newtag)
    msg = "Added!"
    return jsonify(msg)

@app.route("/adminprofile", methods=["GET"])
def adminprofile(diffperson=None):
   
    try:
        print('we made it to profile')
        if diffperson is None:
            diffperson = request.args.get("diffperson")
        print("no diff person", diffperson)
        netid = _cas.authenticate()
        netid = netid.rstrip()

        print("net id found?")
        if diffperson:
            student = get_student_info(diffperson)
        else:
            student = get_student_info(netid)
            diffperson = netid
        
        isAdmin = 0
        if student.admin:
            isAdmin = 1

        name = student.name
        classyear = student.year
        major = student.major
        clubs = student.clubs
        bio = student.bio
        interests = student.tags
        tags = get_all_tags()

        html = render_template("adminprofile.html", student = student,  name=name, netid= netid,
        classyear=classyear, major=major, clubs=clubs, tags=tags,
        bio=bio, interests=interests, diffperson = diffperson, isAdmin = isAdmin)

        response = make_response(html)
        return response
    except Exception:
        print("whoops from profile")

# rendering edit profile page from the profile page
@app.route("/admineditprofile", methods=["GET"])
def admineditprofile():
    adminnetid = _cas.authenticate()
    adminnetid = adminnetid.rstrip()
    
    studentnetid = request.args.get("netid")
    
    student = get_student_info(studentnetid)
    admin = get_student_info(adminnetid)

    isAdmin = 0
    if admin.admin:
        isAdmin = 1
    
    name = student.name
    classyear = student.year
    major = student.major
    bio = student.bio
    clubs = get_all_clubs()
    tags = get_all_tags()
    try:
        html = render_template("admineditprofile.html", name=name, netid=studentnetid, student = student, clubs = clubs, tags = tags,
        classyear=classyear, major=major,
        bio=bio, isAdmin = isAdmin)
        response = make_response(html)
        return response
    except Exception:
        print("whoops from admineditprofile")

@app.route("/blackliststudent", methods=["GET"])
def blackliststudent():
    adminnetid = _cas.authenticate()
    adminnetid = adminnetid.rstrip()
    
    studentnetid = request.args.get("studentnetid")

    blacklist_student(studentnetid)
    msg = "Blacklisted"
    return jsonify(msg)

@app.route("/whiteliststudent", methods=["GET"])
def whiteliststudent():
    adminnetid = _cas.authenticate()
    adminnetid = adminnetid.rstrip()
    
    studentnetid = request.args.get("studentnetid")

    whitelist_student(studentnetid)
    msg = "Whitelisted"
    return jsonify(msg)

@app.route("/getstudentsJSON", methods=["POST", "GET"])
def students_json():
    if request.method == 'GET':
        students = get_all_students()
        students_json = []
        for student in students:
            each_student = {
                'id':student.netid,
                'text':student.netid}
            print(student.netid)
            students_json.append(each_student)
        return jsonify(students_json)
    else:
        return None
