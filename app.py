from flask import Flask, g, session, redirect, request, render_template, url_for, send_file
import os
import pymongo


app = Flask(__name__)

app.secret_key = os.urandom(24)

@app.route("/")
def index():
    return "Test"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

if __name__ == "__main__":
    app.run()