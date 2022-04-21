from functools import wraps
from fastapi import FastAPI, Request
import fastapi
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from app import app
from user.models import UserCommands, User



@app.post('/api/v1/user/register')
async def signup(user:User):
    return await UserCommands().register(user)

# @app.route('/user/signout', methods = ['GET'])
# async def signout():
#     return await User().signout()

@app.post('/api/v1/user/login')
async def login(form: OAuth2PasswordBearer = fastapi.Depends()):
    return await UserCommands().login(form.email, form.password)
