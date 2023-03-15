from flask import Flask, g, session, redirect, request, render_template, url_for, send_file
import os
import pymongo
from decouple import config

app = Flask(__name__)

app.secret_key = os.urandom(24)

MONGODB_URI = config('MONGODB_URI')
client = pymongo.MongoClient(MONGODB_URI)
db = client['automl']
users = db['users']

@app.before_request
def before_request():
    g.user = None 
    if 'user' in session:
        g.user = session['user']


@app.route("/")
def index():
    if request.method == "GET":
        if g.user:
            return render_template("index.html",username=session['user'])
        return redirect(url_for('login'))

@app.route('/login',methods=['GET', 'POST'])
def login():
    global invalid_user
    if request.method == 'POST':
        session.pop('user',None)
        user_list = users.find_one({"username":request.form['username']})
        if user_list:
            if request.form['password'] == user_list['password']:
                session['user'] = request.form['username']
                # return render_template('index.html',username=session['user'])
                return redirect(url_for('index',username=session['user']))
            return render_template('login.html',invalid_user="Invalid Username or Password")
        return render_template('login.html',invalid_user="Invalid Username or Password")
    return render_template('login.html')

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    global username_taken_msg
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user_list = users.find_one({"username":username})
        if user_list:
            username_taken_msg = "Username already taken, try another one"
            return render_template('signup.html',username_taken_msg=username_taken_msg)
        users.insert_one({"username":username,"password":password})
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)