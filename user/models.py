from fastapi import FastAPI, Request, Security
import fastapi
from passlib.hash import pbkdf2_sha256
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
import uuid
import os
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel
import jwt
from app import cluster
load_dotenv(find_dotenv())

JWT_SECRET = os.environ.get('SECRET_KEY')
oauth2schema = OAuth2PasswordBearer(tokenUrl='/api/v1/user/login')

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
            # 'token': access_security.create_access_token(subject={'email':user['email'], 'password':user['password']})
        }

        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        if user_collection.find_one({"email":user['email']}):
            raise HTTPException(status_code=400, detail='Email already in use')

        if user_collection.find_one({"username":user['username']}):
            raise HTTPException(status_code=400, detail='Username already in base')

        try:
            user_collection.insert_one(user)
        except:
            raise HTTPException(status_code=400, detail='Sign up failed. Contact administration')
        return await self.get_token(user)

        

    async def get_token(self, user:dict):
        token = jwt.encode(user, JWT_SECRET)
        return dict(access_token = token)

    async def login(self, email:str, password:str):

        user = user_collection.find_one({'email':email})

        if user is None:
            raise HTTPException(status_code=401, detail='No such email')

        if user and pbkdf2_sha256.verify(password, user['password']):
            return await self.get_token(user)

        raise HTTPException(status_code=401, detail='Ivalid login data')

    async def get_user_by_token(self,token:str = fastapi.Depends(oauth2schema)):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            user = user_collection.find_one({'_id':payload['_id']})

        except:
            raise HTTPException(status_code=401, detail='Ivalid email or password')
        
        return user