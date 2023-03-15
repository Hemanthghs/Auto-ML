from flask import Flask, g, session, redirect, request, render_template, url_for, send_file
import os
import pymongo
from decouple import config
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
import joblib

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

@app.route("/classify")
def classify():
    return render_template("classify.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('login.html')

@app.route('/upload', methods=["POST", "GET"])
def upload():
    global classes
    if g.user:
        global path
        inputs = request.files["inputs"]
        fname = inputs.filename
        print(os.path)
        path = os.path.join('data',fname)
        inputs.save(path)

        outputs = request.files["outputs"]
        fname = outputs.filename
        print(os.path)
        path = os.path.join('data',fname)
        outputs.save(path)

        page = request.args.get("type")
        classes = "Data Description"


        return render_template("classify.html", toast = "success", username=session['user'], classes=classes)
    return redirect(url_for('login'))


@app.route("/train", methods=["POST"])
def train():
    model = request.form["model"]
    if model == "logistic":
        logistic_model()
    return "Started training" + model

def logistic_model():
    X = pd.read_csv("inputs.csv")
    y = pd.read_csv("outputs.csv")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    joblib.dump("models/log_model.sav")
    return "Training completed"




if __name__ == "__main__":
    app.run(debug=True)