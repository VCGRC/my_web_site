from functools import wraps
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from app import app
from user.models import UserCommands, User



@app.post('/api/v1/user/register')
async def signup(user:User):
    return await UserCommands().register(user)

# @app.route('/user/signout', methods = ['GET'])
# async def signout():
#     return await User().signout()

@app.post('/api/v1/user/login')
async def login_back(email:str, password:str):
    return await UserCommands().login(email, password)
