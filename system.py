from flask import (
    Flask,
    render_template,
    url_for,
    request,
    redirect,
)
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
from form import LoginForm, PredictForm
import pickle

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.secret_key = str(os.urandom(24))
db = SQLAlchemy(app)

global_user = None
remember_me = False
data = None
base_intrest_rate=15
plot_list = [
    [0,81.78, 65.43, 59.85, 75.46, 10.78, 313971.9, 123059.91, 10470.76, 360, 84.94, 1],
    [1,100.0, 85.71, 28.57, 100.0, 14.29, 3963554.29, 54285.71, 30651.43, 360, 71.43, 1],
    [2,75.0, 25.0, 50.0, 100.0, 25.0, 127040.0, 2310080.0, 15640.0, 360, 100.0, 2],
    [3,80.0, 64.62, 52.31, 96.92, 33.85, 1049969.23, 58600.62, 19713.52, 360, 90.77, 2],
]


class admin(db.Model):
    username = db.Column(db.String(30), primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.password}')"


def prediction(data):
    global base_intrest_rate
    
    with open("svm_predict.pkl", "rb") as file:
        svm = pickle.load(file)
        model = svm["model"]
        scaler = svm["scaler"]
    data = [
        int(data["gender"]),
        data["married"],
        int(data["dependents"]),
        int(data["education"]),
        data["self_employed"],
        data["income"],
        data["co_applicant_income"],
        data["loan_amount"],
        data["loan_amount_term"],
        data["credit_history"],
        data["property_area"],
    ]
    result = model.predict(scaler.transform([data]))[0]
    intrest_rate=base_intrest_rate+(1-result)*base_intrest_rate
    return (result,intrest_rate)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        user_email = form.email.data
        pass_word = form.password.data
        login_user = admin.query.filter_by(
            username=user_name, email=user_email, password=pass_word
        ).first()

        if login_user:
            global global_user, remember_me
            global_user = user_name
            remember_me = form.remember.data
            return redirect(f"/home/{user_name}")
        else:
            return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route("/home/<string:username>")
def home(username: str):
    global global_user
    if global_user == username:
        global_user = None if not remember_me else global_user
        return render_template("home.html", username=username, list=plot_list)
    else:
        return redirect("/login")


@app.route("/predict", methods=["POST", "GET"])
def predict():
    form = PredictForm()
    if form.validate_on_submit():
        global data
        data = form.data
        return redirect(url_for("result"))
    return render_template("predict.html", form=form)


@app.route("/result")
def result():
    # try:
    result,ir=prediction(data)
    per_day=(data["loan_amount"]*(1.0+(ir/100)))/float(data["loan_amount_term"])
    return render_template("result.html", result=round(result,4),intrest_rate=round(ir,2),per_day=round(per_day,2))
    # except:
    #     return redirect(url_for("predict"))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
