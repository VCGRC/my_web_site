from fastapi import FastAPI, Request, Security
from passlib.hash import pbkdf2_sha256
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
import uuid
import os
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer
from app import cluster
load_dotenv(find_dotenv())

access_security = JwtAccessBearer(secret_key=os.environ.get('SECRET_KEY'), auto_error=True)
user_collection = cluster.web.users

class User(BaseModel):
    _id: str
    name: str
    email: str
    username: str
    password: str
    access_level: int

class UserCommands:

    async def register(self, man:User):

        data = man
        user = {
            "_id":uuid.uuid4().hex,
            "name":data.name,
            "email":data.email,
            "username":data.username,
            "password":data.password,
            "access_level":0
        }

        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        if user_collection.find_one({"email":user['email']}):
            raise HTTPException(status_code=400, detail='Email already in use')

        if user_collection.find_one({"username":user['username']}):
            raise HTTPException(status_code=400, detail='Username already in base')

        if user_collection.insert_one(user):
            return jsonable_encoder(user)

        raise HTTPException(status_code=400, detail='Sign up failed. Contact administration')

    async def get_token(self, user:dict):
        token = access_security.create_access_token(subject={'email':user['email'], 'password':user['password']})
        return dict(access_token = token)

    async def login(self, email:str, password:str):

        user = user_collection.find_one({'email':email})

        if user is None:
            raise HTTPException(status_code=401, detail='No such email')

        if user and pbkdf2_sha256.verify(password, user['password']):
            return await self.get_token(user)

        raise HTTPException(status_code=401, detail='Ivalid login data')