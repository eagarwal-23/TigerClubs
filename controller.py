from flask import Flask, request, make_response
from flask import render_template

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
    # profile_informations = get_profile_information(netid)
    html = render_template("profile.html", netid=)
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

@app.route("/editprofile", methods=["GET"])
def editprofile():
    # profile_information = get_profile_information(netid)
    html = render_template("editprofile.html")
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
    