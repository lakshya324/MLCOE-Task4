from flask import Flask, render_template, url_for,request,redirect,flash,get_flashed_messages,Response
from flask_sqlalchemy import SQLAlchemy
import datetime , time
import cv2
import os
import numpy as np
from form import LoginForm,PredictForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.secret_key=str(os.urandom(24))
db=SQLAlchemy(app)

global_user=None
remember_me=False
data=None
result=None

class admin(db.Model):
    username=db.Column(db.String(30),primary_key=True)
    email=db.Column(db.String(30),unique=True,nullable=False)
    password=db.Column(db.String(30),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.datetime.now)
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.password}')"

def prediction(data):
    #TODO: Write code for prediction
    #name=form.name.data
    #gender=int(form.gender.data)
    #income=form.income.data
    #co_applicant_income=form.co_applicant_income.data
    #loan_amount=form.loan_amount.data
    #loan_amount_term=int(form.loan_amount_term.data)
    #credit_history=int(form.credit_history.data)
    #dependents=int(form.dependents.data)
    #education=int(form.education.data)
    #self_employed=form.self_employed.data
    #married=form.married.data
    #property_area=int(form.property_area.data)
    global result 
    result=1


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user_name=form.username.data
        user_email=form.email.data
        pass_word = form.password.data
        login_user = admin.query.filter_by(username=user_name,email=user_email, password=pass_word).first()
        
        
        if login_user:
            global global_user,remember_me
            global_user=user_name
            remember_me=form.remember.data
            return redirect(f'/home/{user_name}')
        else:
            return redirect(url_for('login'))
    return render_template('login.html',form=form)


@app.route('/home/<string:username>')
def home(username:str):
    global global_user
    if global_user==username:
        global_user=None if not remember_me else global_user
        return render_template('home.html',username=username)
    else:
        return redirect('/login')

@app.route('/predict',methods=['POST','GET'])
def predict():
    form=PredictForm()
    if form.validate_on_submit():
        global data
        data=form.data
        return redirect(url_for('result'))
    return render_template('predict.html',form=form)

@app.route('/result')
def result():
    global data
    prediction(data)
    return render_template('result.html',result=result)

if __name__=="__main__":
    app.run(debug=True)
