from functools import wraps
from quart import Quart, redirect, render_template, session, request, url_for
from app import app
from user.models import User
from decorators import login_required, access_level

@app.route('/registration/', methods = ['GET'])
async def registration():
    return render_template('signup.html')

@app.route('/profile/', methods = ['GET'])
@login_required
async def profile():
    return render_template('profile.html')

@app.route('/user/signup', methods = ['POST'])
async def signup():
    return User().signup()

@app.route('/user/signout', methods = ['GET'])
async def signout():
    return User().signout()

@app.route('/user/login', methods = ['POST'])
async def login_back():
    return User().login()

@app.route('/login/', methods = ['GET'])
async def login():
    return render_template('login.html')