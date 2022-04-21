from functools import wraps
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from app import app
from user.models import UserCommands



@app.post('/api/v1/user/register', methods = ['POST'])
async def signup(request:Request):
    return await UserCommands().register(request)

# @app.route('/user/signout', methods = ['GET'])
# async def signout():
#     return await User().signout()

# @app.route('/user/login', methods = ['POST'])
# async def login_back():
#     return await User().login()
