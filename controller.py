from flask import Flask, request, make_response
from flask import render_template


app = Flask(__name__, template_folder=".")

@app.route("/", methods=["GET"])
@app.route("/login", methods=["GET"])
def login():

@app.route("/landing", methods=["GET"])
def landing():


@app.route("/profile", methods=["GET"])
def profile():

@app.route("/editprofile", method=["GET"])
def editprofile():
    