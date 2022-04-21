from functools import wraps
from fastapi import FastAPI, Request, Security
import fastapi
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app import app
import os
from dotenv import load_dotenv, find_dotenv
from user.models import UserCommands, User

oauth2schema = OAuth2PasswordBearer(tokenUrl='/api/v1/user/me')


@app.post('/api/v1/user/register')
async def signup(user:User):
    return await UserCommands().register(user)

# @app.route('/user/signout', methods = ['GET'])
# async def signout():
#     return await User().signout()

@app.post('/api/v1/user/login')
async def login(form: OAuth2PasswordRequestForm = fastapi.Depends()):
    return await UserCommands().login(form.username, form.password)


@app.get('/api/v1/user/me')
async def get_me(token:fastapi.Depends(oauth2schema)):
    return await UserCommands().get_user_by_token(token)
