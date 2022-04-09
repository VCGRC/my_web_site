from functools import wraps
from flask import Flask, redirect, render_template, session, request, url_for
from app import app

async def login_required(f):
    @wraps(f)
    async def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return await f(*args, **kwargs)
        else:
            return await redirect('/')

    return wrap

async def access_level(level = 0):
    async def decorator(f):
        @wraps(f)
        async def wrap(*args, **kwargs):
            if 'logged_in' in session:
                if session['user']['access_level']>=level:
                    return await f(*args, **kwargs)
                else:
                    return  await redirect('/')
            else:
                return await redirect('/') 
        return await wrap
    return await decorator