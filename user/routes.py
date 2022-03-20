from functools import wraps
from flask import Flask, redirect, render_template, session, request
from app import app
from user.models import User
from decorators import login_required, access_level

@app.route('/registration/', methods = ['GET'])
def registration():
    return render_template('signup.html')

@app.route('/profile/', methods = ['GET'])
@login_required
def profile():
    return render_template('profile.html')

@app.route('/user/signup', methods = ['POST'])
def signup():
    return User().signup()

@app.route('/user/signout', methods = ['GET'])
def signout():
    return User().signout()

@app.route('/user/login', methods = ['POST'])
def login_back():
    return User().login()

@app.route('/login/', methods = ['GET'])
def login():
    return render_template('login.html')