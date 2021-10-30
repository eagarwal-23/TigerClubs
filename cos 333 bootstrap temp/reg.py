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
        print("Whoops from login")

@app.route("/landing", methods=["GET"])
def landing():
    try:
        netid = request.args.get("netid")

        html = render_template("landing.html", netid = netid)
        response = make_response(html)
        return response
    except Exception:
        print("Whoops from landing")

