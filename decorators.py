from functools import wraps
from flask import Flask, redirect, render_template, session, request, url_for
from app import app
# from quart_auth import login_required

def login_required(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect('/')
        else:
            return await fn(*args, **kwargs)

    return wrapper

# def login_required(f):
#     @wraps(f)
#     async def wrap(*args, **kwargs):
#         session = await session
#         if 'logged_in' in session:
#             return await f(*args, **kwargs)
#         else:
#             return await redirect('/')

#     return wrap

def access_level(level = 0):
    def decorator(f):
        @wraps(f)
        async def wrap(*args, **kwargs):
            if 'logged_in' in session:
                if session['user']['access_level']>=level:
                    return await f(*args, **kwargs)
                else:
                    return  await redirect('/')
            else:
                return await redirect('/') 
        return wrap
    return decorator