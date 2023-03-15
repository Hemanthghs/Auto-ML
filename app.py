from flask import Flask, g, session, redirect, request, render_template, url_for, send_file
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)

@app.route("/")
def index():
    return "Test"


if __name__ == "__main__":
    app.run()