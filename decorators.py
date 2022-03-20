from functools import wraps
from flask import Flask, redirect, render_template, session, request
from app import app

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')

    return wrap

def access_level(level = 0):
    def decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if 'logged_in' in session:
                if session['user']['access_level']>=level:
                    return f(*args, **kwargs)
                else:
                    return redirect('/')
            else:
                return redirect('/') 
        return wrap
    return decorator