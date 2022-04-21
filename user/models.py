from fastapi import FastAPI, Request
from passlib.hash import pbkdf2_sha256
from fastapi.encoders import jsonable_encoder
import uuid
from pydantic import BaseModel
from app import cluster

user_collection = cluster.web.users

class User(BaseModel):
    _id: str
    name: str
    email: str
    username: str
    password: str
    access_level: int

class UserCommands:

    async def register(self, user:User):

        data = user
        user = {
            "_id":uuid.uuid4().hex,
            "name":data['name'],
            "email":data['email'],
            "username":data['username'],
            "password":data['password'],
            "access_level":0
        }

        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        if user_collection.find_one({"email":user['email']}):
            return jsonable_encoder({"error":"Email already in base"}), 400

        if user_collection.find_one({"username":user['username']}):
            return jsonable_encoder({"error":"Username already in base"}), 400

        if await user_collection.insert_one(user):
            return jsonable_encoder(user)

        return jsonable_encoder({"error":"Sign up failed. Contact administration"}), 400

    # async def signout(self):
    #     session.clear()
    #     return redirect('/')

    # async def login(self):

    #     data = await request.form
    #     user = user_collection.find_one({'email':data['email']})

    #     if user and pbkdf2_sha256.verify(data['password'], user['password']):
    #         return await self.start_session(user)

    #     return jsonify({'error':"Ivalid login data"}), 401