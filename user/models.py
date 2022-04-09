from quart import Quart, jsonify, redirect, request, session
from passlib.hash import pbkdf2_sha256
import uuid
from app import cluster

user_collection = cluster.web.users

class User:

    async def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200


    async def signup(self):

        user = {
            "_id":uuid.uuid4().hex,
            "name":request.form.get('name'),
            "email":request.form.get('email'),
            "username":request.form.get('username'),
            "password":request.form.get('password'),
            "access_level":0
        }

        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        if user_collection.find_one({"email":user['email']}):
            return jsonify({"error":"Email already in base"}), 400

        if user_collection.find_one({"username":user['username']}):
            return jsonify({"error":"Username already in base"}), 400

        if user_collection.insert_one(user):
            return self.start_session(user)

        return jsonify({"error":"Sign up failed. Contact administration"}), 400

    async def signout(self):
        session.clear()
        return redirect('/')

    async def login(self):
        user = user_collection.find_one({'email':request.form.get('email')})

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)

        return jsonify({'error':"Ivalid login data"}), 401