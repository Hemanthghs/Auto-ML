from flask import Flask, g, session, redirect, request, render_template, url_for, send_file
import os
import pymongo
from decouple import config
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)

app.secret_key = os.urandom(24)

MONGODB_URI = config('MONGODB_URI')
client = pymongo.MongoClient(MONGODB_URI)
db = client['automl']
users = db['users']
counter = db['counter']
cr_data = db['classification_regression']

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
    if g.user:
        return render_template("classify.html", username = session["user"])
    return redirect(url_for("index"))

@app.route("/regression")
def regression():
    if g.user:
        return render_template("regression.html", username = session["user"])
    return redirect(url_for("index"))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('login.html')

@app.route('/upload', methods=["POST", "GET"])
def upload():
    global classes
    if g.user:
        global path
        username = session['user']
        inputs = request.files["inputs"]
        fname = inputs.filename
        print(os.path)
        input_path = os.path.join('data',fname)
        inputs.save(input_path)

        outputs = request.files["outputs"]
        fname = outputs.filename
        print(os.path)
        output_path = os.path.join('data',fname)
        outputs.save(output_path)

        model_type = request.args.get("type")
        model_data = counter.find_one({"type":"model"})
        model_id = model_data['count'] + 1
        counter.update_one({"type":"model"},{"$set":{"count":model_id}})
        cr_data.insert_one({"username":username,"model_id":model_id,"input_path":input_path, "output_path":output_path, "model_type":model_type})

        #Return to the upload page 
        page = model_type + ".html"


        classes = "Data Description"


        return render_template(page, toast = "success", username=username, classes=classes, model_id = model_id, model_type = model_type)
    return redirect(url_for('login'))


@app.route("/train", methods=["POST"])
def train():
    model_name = request.form["model"]
    model_id = request.args.get("model_id")
    model_type = request.args.get("model_type")
    model_data = cr_data.find_one({"model_id":int(model_id)})
    input_data = model_data["input_path"]
    output_data = model_data["output_path"]
    model_train(input_data, output_data, model_id, model_name, model_type)
    return redirect(url_for("history",model_id=model_id))

def impute_null(data):
    for col in data.columns:
        if data[col].isnull().any():
            if data[col].dtype == "object":
                data[col] = data[col].fillna(data[col].mode()[0])
            else:
                data[col] = data[col].fillna(data[col].mean())
    return data

def encode_data(data):
    le = LabelEncoder()
    encodings = dict()

    for col in data.columns:
        if data[col].dtype == "object":
            data[col] = le.fit_transform(data[col])
            keys = le.classes_
            values = le.transform(le.classes_)
            dictionary = dict(zip(keys, [x.item() for x in values]))
            encodings[col] = dictionary
    return data, encodings

def model_train(input_data, output_data, model_id, model_name, model_type):
    X = pd.read_csv(input_data)
    y = pd.read_csv(output_data)

    X = impute_null(X)
    X, encodings = encode_data(X)

    #Getting meta data
    parameters = [col for col in X.columns]
    inputs_count = len(parameters)
    output_name = y.columns[0]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    if model_type == "classify":
        if model_name == "logistic":
            model = LogisticRegression()
        elif model_name == "decision_tree":
            model = DecisionTreeClassifier()
        elif model_name == "random_forest":
            model = RandomForestClassifier()
        elif model_name == "svm":
            model = SVC()
        else:
            model = KNeighborsClassifier()
    else:
        if model_name == "linear_reg":
            model = LinearRegression()
        elif model_name == "decision_tree_reg":
            model = DecisionTreeRegressor()
        elif model_name == "random_forest_reg":
            model = RandomForestRegressor()
        elif model_name == "svm_reg":
            model = SVR()
        else:
            model = KNeighborsRegressor()
    model.fit(X_train, y_train)
    model_path = "models/"+"model_"+str(model_id)+".sav"
    joblib.dump(model, model_path)
    cr_data.update_one({"model_id":int(model_id)},{"$set":{
        "model_file":model_path,
        "model_name":model_name, 
        "parameters":parameters,
        "inputs_count":inputs_count,
        "output_name": output_name,
        "encodings":encodings
        }})
    return

@app.route("/try_model", methods=["POST","GET"])
def try_model():
    if request.method == "GET":
        model_id = request.args.get("model_id")
        model_data = cr_data.find_one({"model_id":int(model_id)})
        inputs_data = model_data["parameters"]
        output_name = model_data["output_name"]
        return render_template("try_model.html", inputs_data = inputs_data, output_name = output_name, model_id = model_id)
    model_id = request.args.get("model_id")
    model_data = cr_data.find_one({"model_id":int(model_id)})
    model_file = model_data["model_file"]
    values = list(request.form.values())
    values = [float(x) for x in values]
    model = joblib.load(model_file)
    prediction = model.predict([values])
    return "<h1>Prediction: " + str(prediction) + "</h1>"

@app.route("/history")
def history():
    data = []
    if g.user:
        for x in cr_data.find({"username":session["user"]}):
            data.append([
                x["model_id"],
                x["input_path"],
                x["output_path"],
                x["model_file"],
                x["model_type"],
                x["model_name"],
            ])
    
        return render_template("history.html",data = data,username=session['user'])
    return redirect(url_for('login'))
@app.route("/download")
def download():
    model_id = request.args.get("model_id")
    data_type = request.args.get("data")
    model_data = cr_data.find_one({"model_id":int(model_id)})
    if data_type == "input":
        return send_file(model_data["input_path"])
    elif data_type == "output":
        return send_file(model_data["output_path"])
    return send_file(model_data["model_file"])

@app.route("/clear", methods=["POST", "GET"])
def clear():
    if request.method == "POST":
        counter.update_one({"type":"model"},{"$set":{"count":0}})
        cr_data.delete_many({})
        return redirect(url_for('login'))
    return render_template("cleardb.html")

def debug(s):
    print("*"*10)
    print(type(s))
    print(s)
    print("*"*10)


if __name__ == "__main__":
    app.run(debug=True)